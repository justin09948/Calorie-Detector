import torch
from torchvision import models, datasets, transforms
from torch.utils.data import DataLoader

#FUNCTION TO TEST THE PRE TRAINED MODEL
def preTrained():
    model = models.resnet50(pretrained=True) 
    model.eval()


    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_data = datasets.ImageFolder("data/food101/test",transform=transform)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=True)

    correct = 0
    total = 0

    total_batches = len(test_loader)

    with torch.no_grad():
        for batch_id, (images, labels) in enumerate(test_loader):
            images, labels = images.to(torch.device('cpu')), labels.to(torch.device('cpu'))
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            if (batch_id + 1) % 10 == 0 or (batch_id + 1) == total_batches:
                progress = (batch_id + 1) / total_batches * 100
                print(f"Progress: {progress:.2f}%")

    accuracy = correct / total
    return accuracy



#FUNCTION TO TEST THE FINE TUNED MODEL
def trained():
    model = models.resnet50(pretrained = False)
    model.fc = torch.nn.Linear(model.fc.in_features, 101)
    model.load_state_dict(torch.load("C:\\Users\\Justin\\Documents\\Projects Coding\\Calorie Detection\\backend\\ML\\best_model.pth"))
    model.eval()


    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_data = datasets.ImageFolder("data/food101/test",transform=transform)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=True)

    correct = 0
    total = 0

    total_batches = len(test_loader)

    with torch.no_grad():
        for batch_id, (images, labels) in enumerate(test_loader):
            images, labels = images.to(torch.device('cpu')), labels.to(torch.device('cpu'))
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            if (batch_id + 1) % 10 == 0 or (batch_id + 1) == total_batches:
                progress = (batch_id + 1) / total_batches * 100
                print(f"Progress: {progress:.2f}%")

    accuracy = correct / total
    return accuracy

pretrained_accuracy = preTrained()
trained_accuracy = trained()

print(f"Pre-trained Accuracy: {pretrained_accuracy * 100:.2f}%")
print(f"Fine-tuned Accuracy: {trained_accuracy * 100:.2f}%")