# ComfyUI Fashion Workflow - Cog Integration

This repository demonstrates how to deploy a custom ComfyUI workflow using [Cog](https://cog.run), making it accessible as an API on [Replicate](https://replicate.com). The workflow leverages several custom nodes, including `CatVTON`, `SegmentAnythingUltra`, and `SDXL Prompt Styler`, to provide a complete virtual try-on solution.

## Purpose
This project provides an API endpoint for a virtual try-on model using ComfyUI and Cog. The workflow allows users to input images and prompts, and it returns a realistic virtual try-on result by combining multiple images with style prompts.

## Key Features
- **ComfyUI Workflow**: Utilizes ComfyUI for building and running the workflow.
- **Cog Integration**: Deploy the workflow as a production-ready API on Replicate, allowing remote inference.
- **Custom Nodes**: Incorporates custom nodes like `CatVTONWrapper`, `SegmentAnythingUltra`, and `SDXLPromptStyler`.
- **Image and Prompt Input**: Accepts image URLs and prompt strings for processing.
  
## Workflow
The workflow leverages three image inputs and two text-based prompts:
1. **Image Inputs**:
   - Image 1: A full-body image of a person.
   - Image 2: A clothing image (e.g., a shirt).
   - Image 3: A second clothing image (e.g., jeans).
2. **Prompt Inputs**:
   - Prompt 1: Describes the style or category of the first clothing item.
   - Prompt 2: Describes the style or category of the second clothing item.

The workflow processes these inputs to generate a realistic virtual try-on image, combining the user's provided clothing and model images.

## Setup

### Prerequisites
- Docker installed on your machine
- Python 3.10+
- Cog installed (`pip install cog`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/krsnalabs/comfyui-fashion.git
   cd comfyui-fashion
   ```

2. **Install dependencies**:
   Activate the virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install custom nodes**:
   Run the provided script to install the necessary custom nodes:
   ```bash
   ./scripts/install_custom_nodes.py
   ```

### API Setup

1. **Prepare the workflow API**:
   The `workflow_api.json` defines the API format for the workflow. Modify the JSON to include your own images and prompts, or use default values for testing.

2. **Run predictions**:
   You can run a test prediction using the following command:
   ```bash
   cog predict -i image_1_url="https://example.com/image1.jpg" \
               -i image_2_url="https://example.com/image2.jpg" \
               -i image_3_url="https://example.com/image3.jpg" \
               -i prompt_1="shirt" \
               -i prompt_2="pant, belt"
   ```

### Deploying on Replicate

1. **Push the model to Replicate**:
   Once the workflow and custom nodes are set up, you can push the model to Replicate using Cog:
   ```bash
   cog push r8.im/your-username/comfyui-fashion
   ```

2. **Access the API**:
   Once deployed, you can access the API endpoint on Replicate to run your own workflows remotely.

## Credits
This repository is a fork of [fofr/cog-comfyui](https://github.com/fofr/cog-comfyui), with significant modifications to integrate fashion-specific workflows using `CatVTON`, `SDXL Prompt Styler`, and `SegmentAnythingUltra`. The original repository provides a comprehensive base for deploying any ComfyUI workflow on Replicate using Cog.

## License
This project is licensed under the terms of the MIT License. See the [LICENSE](./LICENSE) file for details.

---

This README provides clear instructions on how to use, modify, and deploy the ComfyUI workflow as an API using Cog, while crediting the original fork for its foundational work.