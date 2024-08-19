import os
from PIL import Image
import re
from mainapp.globals.constants import id_token
from mainapp.schemas.extraction_response import ExtractionResponse
from transformers import DonutProcessor
from optimum.onnxruntime import ORTModelForVision2Seq


class PassportExtractionService:
    def __init__(self, checkpoint: str) -> None:
        self.model = ORTModelForVision2Seq.from_pretrained(checkpoint)
        self.model.name_or_path = checkpoint
        self.processor = DonutProcessor.from_pretrained(checkpoint)

    def extract(self, image: Image) -> ExtractionResponse:
        device = os.getenv("DEVICE", "cpu")
        max_length = os.getenv("DIMS", 768)
        
        pixel_values = self.processor(
            image.convert("RGB"), return_tensors="pt"
        ).pixel_values
        pixel_values = pixel_values.to(device)
        task_prompt = os.getenv("ID_TOKEN", "cpu")
        decoder_input_ids = self.processor.tokenizer(
            task_prompt, add_special_tokens=False, return_tensors="pt"
        ).input_ids
        decoder_input_ids = decoder_input_ids.to(device)

        outputs = self.model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=max_length,
            early_stopping=False,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
            bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        seq = self.processor.batch_decode(outputs.sequences)[0]
        seq = seq.replace(self.processor.tokenizer.eos_token, "").replace(
            self.processor.tokenizer.pad_token, ""
        )
        seq = re.sub(
            r"<.*?>", "", seq, count=1
        ).strip() 
        seq = self.processor.token2json(seq)
        return ExtractionResponse(**seq)

