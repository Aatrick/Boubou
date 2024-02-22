import os
import random
import sys
from typing import Sequence, Mapping, Any, Union
import torch


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    """Returns the value at the given index of a sequence or mapping.

    If the object is a sequence (like list or string), returns the value at the given index.
    If the object is a mapping (like a dictionary), returns the value at the index-th key.

    Some return a dictionary, in these cases, we look for the "results" key

    Args:
        obj (Union[Sequence, Mapping]): The object to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the given index.

    Raises:
        IndexError: If the index is out of bounds for the object and the object is not a mapping.
    """
    try:
        return obj[index]
    except KeyError:
        return obj["result"][index]


def find_path(name: str, path: str = None) -> str:
    """
    Recursively looks at parent folders starting from the given path until it finds the given name.
    Returns the path as a Path object if found, or None otherwise.
    """
    # If no path is given, use the current working directory
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory
    return find_path(name, parent_directory)


def add_comfyui_directory_to_sys_path() -> None:
    """
    Add 'ComfyUI' to the sys.path
    """
    comfyui_path = find_path("ComfyUI")
    if comfyui_path is not None and os.path.isdir(comfyui_path):
        sys.path.append(comfyui_path)
        print(f"'{comfyui_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    from main import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        print("Could not find the extra_model_paths config file.")


add_comfyui_directory_to_sys_path()
add_extra_model_paths()


def import_custom_nodes() -> None:
    """Find all custom nodes in the custom_nodes folder and add those node objects to NODE_CLASS_MAPPINGS

    This function sets up a new asyncio event loop, initializes the PromptServer,
    creates a PromptQueue, and initializes the custom nodes.
    """
    import asyncio
    import execution
    from nodes import init_custom_nodes
    import server

    # Creating a new event loop and setting it as the default loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Creating an instance of PromptServer with the loop
    server_instance = server.PromptServer(loop)
    execution.PromptQueue(server_instance)

    # Initializing custom nodes
    init_custom_nodes()


from nodes import (
    SaveImage,
    KSamplerAdvanced,
    LoraLoader,
    NODE_CLASS_MAPPINGS,
    CheckpointLoaderSimple,
    EmptyLatentImage,
    VAEDecode,
)


def gen(phrase, adjectives, w, h):
    import_custom_nodes()
    with torch.inference_mode():
        checkpointloadersimple = CheckpointLoaderSimple()
        checkpointloadersimple_4 = checkpointloadersimple.load_checkpoint(
            ckpt_name="sd_xl_refiner_1.0_0.9vae.safetensors"
        )

        emptylatentimage = EmptyLatentImage()
        emptylatentimage_5 = emptylatentimage.generate(
            width=w, height=h, batch_size=1
        )

        checkpointloadersimple_10 = checkpointloadersimple.load_checkpoint(
            ckpt_name="animagineXLV3_v30.safetensors"
        )

        loraloader = LoraLoader()
        loraloader_239 = loraloader.load_lora(
            lora_name="more_details.safetensors",
            strength_model=1,
            strength_clip=1,
            model=get_value_at_index(checkpointloadersimple_10, 0),
            clip=get_value_at_index(checkpointloadersimple_10, 1),
        )

        cliptextencodesdxl = NODE_CLASS_MAPPINGS["CLIPTextEncodeSDXL"]()
        cliptextencodesdxl_75 = cliptextencodesdxl.encode(
            width=2048,
            height=2048,
            crop_w=0,
            crop_h=0,
            target_width=2048,
            target_height=2048,
            text_g=phrase,
            text_l=adjectives,
            clip=get_value_at_index(loraloader_239, 1),
        )

        cliptextencodesdxlrefiner = NODE_CLASS_MAPPINGS["CLIPTextEncodeSDXLRefiner"]()
        cliptextencodesdxlrefiner_81 = cliptextencodesdxlrefiner.encode(
            ascore=2,
            width=2048,
            height=2048,
            text="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name,",
            clip=get_value_at_index(checkpointloadersimple_4, 1),
        )

        cliptextencodesdxl_82 = cliptextencodesdxl.encode(
            width=2048,
            height=2048,
            crop_w=0,
            crop_h=0,
            target_width=2048,
            target_height=2048,
            text_g="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name,",
            text_l="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name,",
            clip=get_value_at_index(loraloader_239, 1),
        )

        cliptextencodesdxlrefiner_120 = cliptextencodesdxlrefiner.encode(
            ascore=6,
            width=2048,
            height=2048,
            text=adjectives,
            clip=get_value_at_index(checkpointloadersimple_4, 1),
        )

        ksampleradvanced = KSamplerAdvanced()
        vaedecode = VAEDecode()
        saveimage = SaveImage()

        for q in range(1):
            ksampleradvanced_22 = ksampleradvanced.sample(
                add_noise="enable",
                noise_seed=random.randint(1, 2**64),
                steps=28,
                cfg=7,
                sampler_name="euler_ancestral",
                scheduler="normal",
                start_at_step=0,
                end_at_step=28,
                return_with_leftover_noise="enable",
                model=get_value_at_index(loraloader_239, 0),
                positive=get_value_at_index(cliptextencodesdxl_75, 0),
                negative=get_value_at_index(cliptextencodesdxl_82, 0),
                latent_image=get_value_at_index(emptylatentimage_5, 0),
            )

            ksampleradvanced_23 = ksampleradvanced.sample(
                add_noise="disable",
                noise_seed=random.randint(1, 2**64),
                steps=28,
                cfg=7,
                sampler_name="ddim",
                scheduler="normal",
                start_at_step=28,
                end_at_step=1000,
                return_with_leftover_noise="disable",
                model=get_value_at_index(checkpointloadersimple_4, 0),
                positive=get_value_at_index(cliptextencodesdxlrefiner_120, 0),
                negative=get_value_at_index(cliptextencodesdxlrefiner_81, 0),
                latent_image=get_value_at_index(ksampleradvanced_22, 0),
            )

            vaedecode_244 = vaedecode.decode(
                samples=get_value_at_index(ksampleradvanced_22, 0),
                vae=get_value_at_index(checkpointloadersimple_10, 2),
            )

            saveimage_248 = saveimage.save_images(
                filename_prefix="ComfyUI", images=get_value_at_index(vaedecode_244, 0)
            )