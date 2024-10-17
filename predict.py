# An example of how to convert a given API workflow into its own Replicate model
# Replace predict.py with this file when building your own workflow

import os
import mimetypes
import json
import shutil
from typing import List
from cog import BasePredictor, Input, Path
from comfyui import ComfyUI
from cog_model_helpers import optimise_images
from cog_model_helpers import seed as seed_helper

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"
COMFYUI_TEMP_OUTPUT_DIR = "ComfyUI/temp"
ALL_DIRECTORIES = [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]

mimetypes.add_type("image/webp", ".webp")

# Save your example JSON to the same directory as predict.py
api_json_file = "workflow_api.json"

# Force HF offline
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

class Predictor(BasePredictor):
    def setup(self):
        self.comfyUI = ComfyUI("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR, INPUT_DIR)

        # Give a list of weights filenames to download during setup
        with open(api_json_file, "r") as file:
            workflow = json.loads(file.read())
        self.comfyUI.handle_weights(
            workflow,
            weights_to_download=[],
        )

    def filename_with_extension(self, input_file, prefix):
        extension = os.path.splitext(input_file.name)[1]
        return f"{prefix}{extension}"

    def handle_input_file(
        self,
        input_file: Path,
        filename: str = "image.png",
    ):
        shutil.copy(input_file, os.path.join(INPUT_DIR, filename))

    def update_workflow(self, workflow, **kwargs):
        # Update the image URLs for the three images
        workflow["10"]["inputs"]["image"] = kwargs["image_1_url"]
        workflow["11"]["inputs"]["image"] = kwargs["image_2_url"]
        workflow["16"]["inputs"]["image"] = kwargs["image_3_url"]
        
        # Update the prompts
        workflow["22"]["inputs"]["text_positive"] = kwargs["prompt_1"]
        workflow["24"]["inputs"]["text_positive"] = kwargs["prompt_2"]
        
        # Update any other workflow-specific parameters, if needed
        workflow["14"]["inputs"]["seed"] = kwargs["seed"]  # Example of setting a seed

    def predict(
        self,
        image_1_url: str = Input(description="URL for the first image"),
        image_2_url: str = Input(description="URL for the second image"),
        image_3_url: str = Input(description="URL for the third image"),
        prompt_1: str = Input(default="shirt", description="First prompt for the text input"),
        prompt_2: str = Input(default="pant, belt", description="Second prompt for the text input"),
        seed: int = seed_helper.predict_seed(),
        output_format: str = optimise_images.predict_output_format(),
        output_quality: int = optimise_images.predict_output_quality(),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        self.comfyUI.cleanup(ALL_DIRECTORIES)

        # Ensure the seed is set
        seed = seed_helper.generate(seed)

        # Load and update the workflow with the input images and prompts
        with open(api_json_file, "r") as file:
            workflow = json.loads(file.read())

        self.update_workflow(
            workflow,
            image_1_url=image_1_url,
            image_2_url=image_2_url,
            image_3_url=image_3_url,
            prompt_1=prompt_1,
            prompt_2=prompt_2,
            seed=seed,
        )

        # Load and run the workflow in ComfyUI
        wf = self.comfyUI.load_workflow(workflow)
        self.comfyUI.connect()
        self.comfyUI.run_workflow(wf)

        # Optimise the generated images and return the paths
        return optimise_images.optimise_image_files(
            output_format, output_quality, self.comfyUI.get_files(OUTPUT_DIR)
        )