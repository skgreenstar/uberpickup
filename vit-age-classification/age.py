import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import torch

from transformers import ViTFeatureExtractor, ViTForImageClassification

# # Init model, transforms
# model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
# transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')

@st.cache_resource
def get_model_transforms():
    model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
    transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')
    return model, transforms

model, transforms = get_model_transforms()

st.title('나이를 맞춰봅시다.')

file_name = st.file_uploader('나이를 예측할 사람의 이미지를 업로드하세요.', type=['png', 'jpg', 'jpeg'])

if file_name is not None:
    image = Image.open(file_name)
    st.image(image, use_column_width=True)

    # Transform our image and pass it through the model
    inputs = transforms(image, return_tensors='pt')
    output = model(**inputs)

    # Predicted Class probabilities
    proba = output.logits.softmax(1)

    # Predicted Classes
    preds = proba.argmax(1)

    values, indices = torch.topk(proba, k=5)

    result_dict = {model.config.id2label[i.item()]: v.item() for i, v in zip(indices.numpy()[0], values.detach().numpy()[0])}
    first_result = list(result_dict.keys())[0]

    print(f'predicted result:{result_dict}')
    print(f'1st: {first_result}')

    st.header('결과')
    st.subheader(f'예측된 나이: {first_result}')

    for k, v in result_dict.items():
        st.write(f'{k}: {v * 100:.2f}%')
