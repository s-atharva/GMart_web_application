def get_image_path(raw_path: str):
    largest_item = ""
    for item in raw_path.split("/"):
        if len(largest_item) < len(item):
            largest_item = item

    return f"https://drive.google.com/uc?id={largest_item}"
