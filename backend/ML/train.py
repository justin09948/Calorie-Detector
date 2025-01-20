import torch
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader

model = models.resnet50(pretrained = True)

for layer in model.parameters():
    layer.requires_grad = False

model.fc = torch.nn.Linear(model.fc.in_features, 101)

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_data = datasets.ImageFolder("data/food101/train",transform=transform)

train_loader = DataLoader(train_data, batch_size=16, shuffle=True)

loss_fn = torch.nn.CrossEntropyLoss()
optomizer = torch.optim.Adam(model.fc.parameters(), lr = 0.001)

model.to(torch.device("cpu"))
best_loss = float('inf')
model.train()
for epoch in range(20):
    total_loss = 0
    for images,labels in train_loader:
        images = images.to(torch.device("cpu"))
        labels = labels.to(torch.device("cpu"))

        outputs = model(images)

        loss = loss_fn(outputs, labels)

        optomizer.zero_grad()
        loss.backward()

        optomizer.step()

        total_loss += loss.item()
    
    avg_loss = total_loss / len(train_loader.dataset)

    print(f"Epoch {epoch+1}/20, Total Loss: {total_loss:.4f}, Average Loss: {avg_loss:.4f}")

    torch.save(model.state_dict(), f"model_epoch_{epoch+1}.pth")

    if avg_loss < best_loss:
        best_loss = avg_loss
        torch.save(model.state_dict(), "best_model.pth")