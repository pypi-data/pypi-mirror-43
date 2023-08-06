from starfish.pipeline.algorithmbase import AlgorithmBase


class DecoderAlgorithmBase(AlgorithmBase):
    def run(self, encoded, codebook):
        """Performs decoding on the spots found, using the codebook specified."""
        raise NotImplementedError()
