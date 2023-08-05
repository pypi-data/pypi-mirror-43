from collections import Counter
import os


def _string_split(strings, delimiter=" ", pad_value="<PAD>"):
    """Get a padded string tensor by splitting the given string tensor.

    Args
        strings (Tensor): a 1D Tensor of dtype string.

    Keyword args
        delimiter (str): how to split. If set to '', will split by characters.
        pad_value (str): string to use for padding.

    Returns
        Tensor: a 2D Tensor of dtype string.

    """
    original_shape = tf.shape(strings)
    if len(strings.shape) == 0:
        strings = tf.expand_dims(strings, 0)
    sp = tf.string_split(strings, delimiter=delimiter)  # a SparseTensor.
    return tf.sparse.to_dense(sp, default_value=pad_value)


class TextInput(Input):
    """Abstract input pipeline for textual datasets.

    Optional overridables
        build_mapping

    """

    def __init__(self, files, mapping=None, **kwargs):
        """Constructor.

        Textual datasets require to make a type <-> id mapping to be used. In
        order to avoid re-building it every single time, it will be saved to
        `~/.tfbuild/mapping/<mapping_name>.txt`.

        Args
            files (str/list): either a directory path or a list of paths.

        Keyword args
            mapping (str): the file name (minus extension) where the
                type <-> id mapping will be saved.

        """
        super().__init__(**kwargs)

        if type(files) == str:
            files = [os.path.join(files, f) for f in os.listdir(files)]

        self._file_paths = files
        self._mapping_name = mapping
        self._type_to_id = None

    @property
    def file_paths(self):
        return self._file_paths

    @property
    def mapping_name(self):
        return self._mapping_name

    @property
    def type_to_id(self):
        return self._type_to_id

    def build_mapping(self):
        """Create the type <-> id mapping. Overridable.

        Returns
            function: takes a string argument and returns the graph operation that
                applies the mapping to the string.
        """
        pass

    def read_data(self):
        return tf.data.TextLineDataset(self.file_paths)

    # Overriden to apply the type <-> id mapping AFTER batching, since the batches need
    # to be padded to the length of the longest sequence in the batch.
    def _build_dataset(self, dataset):
        super()._build_dataset(dataset)

        mapping_fn = self.build_mapping()
        if mapping_fn is not None:
            self._type_to_id = mapping_fn
            self._dataset = self._dataset.map(
                self.type_to_id, num_parallel_calls=self._num_parallel_calls
            )


class WordInput(TextInput):
    """Input pipeline that creates an id mapping for words."""

    default_hparams = {"batch_size": 16, "vocabulary_size": 20000}

    def build_mapping(self):
        mapping_path = os.path.join(get_mapping_dir(), self.mapping_name + ".txt")

        if not os.path.isfile(mapping_path):
            print(f"INFO: Building new word mapping at `{mapping_path}`")
            word_counts = Counter()

            for file_path in self.file_paths:
                with open(file_path) as f:
                    for line in f:
                        for word in line.split():
                            word_counts.update((word,))

            with open(mapping_path, "w") as f:
                f.write("<PAD>\n<UNK>\n<SOS>\n<EOS>\n")
                for word, _ in word_counts.most_common(
                    self.hparams.vocabulary_size - 4
                ):
                    f.write(word + "\n")

        print(f"INFO: Reading word mapping at `{mapping_path}`")

        # TensorFlow bug: using `reuse=tf.AUTO_REUSE` in `tf.variable_scope` won't
        # reuse the tables, so we have to manually check for their existence to
        # avoid duplicating the mapping in RAM.
        with tf.variable_scope(f"{name}_mapping", reuse=tf.AUTO_REUSE):
            word_to_id = tf.contrib.lookup.index_table_from_file(
                mapping_path,
                vocab_size=self.hparams.vocabulary_size,
                default_value=1,
                name="word_to_id",
            )

        return lambda x: word_to_id.lookup(_string_split(x))


# TODO: add the option to group the characters by word with an extra dimension.
class CharInput(TextInput):
    """Input pipeline that creates an id mapping for characters.

    Example use cases include any purely character-based models, as well as
    models that create word embeddings from the word's characters (e.g. ELMo).

    """

    def __init__(self, files, group_by_word=False, **kwargs):
        """Constructor.

        Keyword args
            group_by_word (bool): if true, input tensors will have shape
                [batch_size, max_chars_per_word, vocabulary_size], with the new middle
                dimension padded with zeros.

        """
        super().__init__(files, **kwargs)
        self._group_by_word = group_by_word

    def build_mapping(self):
        mapping_path = os.path.join(get_mapping_dir(), name + ".txt")

        if not os.path.isfile(mapping_path):
            print(f"INFO: Building new char mapping at `{mapping_path}`")
            char_to_id = {}

            for file_path in self.file_paths:
                with open(file_path) as f:
                    for line in f:
                        for char in line:
                            char_to_id[char] = 0  # value is irrelevant

            with open(mapping_path, "w") as f:
                f.write("<PAD>\n<UNK>\n<SOS>\n<EOS>\n")
                for char in char_to_id.keys():
                    f.write(char + "\n")

        print(f"INFO: Reading char mapping at `{mapping_path}`")
        with tf.variable_scope(f"{name}_mapping", reuse=tf.AUTO_REUSE):

            char_to_id = tf.contrib.lookup.index_table_from_file(
                mapping_path,
                vocab_size=len(char_to_id) + 4,
                default_value=1,
                name="char_to_id",
            )

        if self._group_by_word:
            return lambda x: char_to_id.lookup(
                _string_split(_string_split(x), delimiter="")
            )

        return lambda x: char_to_id.lookup(_string_split(x, delimiter=""))
