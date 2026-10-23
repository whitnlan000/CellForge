import pygame,random
import numpy as np
#SCREEN = pygame.display.set_mode((200,200))

array = np.full((100,100), "form1", dtype=object)

print(array)
import hashlib


def word_to_color(word: str) -> str:
  # Create an MD5 or SHA-256 hash of the word
  hash_bytes = hashlib.md5(word.encode("utf-8")).digest()

  # Take the first 3 bytes for Red, Green, and Blue
  r, g, b = hash_bytes[0], hash_bytes[1], hash_bytes[2]

  # Convert to a hex color string
  return f"#{r:02x}{g:02x}{b:02x}"


def tick():
    SCREEN.fill((0,0,0))
    for x,ix in enumerate(array):
        for y,iy in enumerate(ix):
            screen_w, screen_h = SCREEN.get_size()
            cell_w = screen_w / array.shape[1]
            cell_h = screen_h / array.shape[0]

            rect = pygame.Rect(
                x * cell_w,
                y * cell_h,
                cell_w,
                cell_h
            )

            pygame.draw.rect(SCREEN, word_to_color(iy), rect, 0)
            pygame.draw.rect(SCREEN, (128,128,128), rect, 1)

    pygame.display.flip()