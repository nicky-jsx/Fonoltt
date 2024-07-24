import pygame
import csv

WIDTH, HEIGHT = 1024, 768
FPS = 60
COLOURS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255)

}
TIMER = 30  # seconds

def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        print(f"Unable to load image: {filename}")
        return pygame.Surface((100, 100))  # Return a blank surface as a fallback

def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except pygame.error:
        print(f"Unable to load sound: {filename}")
        return None  # Return None as a fallback

def load_links_from_csv(filepath):
    links = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            links.append({
                'text': row['link'],
                'is_legit': row['is_legit'].lower() == 'true'
            })
    return links