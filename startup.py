import pygame

width = 20
height = 20

def run():
    global width, height

    pygame.init()

    screen = pygame.display.set_mode((500, 250))
    pygame.display.set_caption("CellForge Setup")

    font = pygame.font.SysFont(None, 30)

    width_slider = pygame.Rect(150, 50, 250, 10)
    height_slider = pygame.Rect(150, 100, 250, 10)

    start_button = pygame.Rect(175, 170, 150, 50)

    dragging_width = False
    dragging_height = False

    running = True

    while running:
        screen.fill((40, 40, 40))

        mx, my = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (100, 100, 100), width_slider)
        pygame.draw.rect(screen, (100, 100, 100), height_slider)

        width_x = width_slider.x + ((width - 1) / 59) * width_slider.w
        height_x = height_slider.x + ((height - 1) / 59) * height_slider.w

        pygame.draw.circle(screen, (255, 255, 255), (int(width_x), 55), 10)
        pygame.draw.circle(screen, (255, 255, 255), (int(height_x), 105), 10)

        screen.blit(
            font.render(f"Width: {width}", True, (255, 255, 255)),
            (20, 40)
        )

        screen.blit(
            font.render(f"Height: {height}", True, (255, 255, 255)),
            (20, 90)
        )

        pygame.draw.rect(screen, (0, 150, 0), start_button)

        text = font.render("START", True, (255, 255, 255))
        screen.blit(
            text,
            (
                start_button.centerx - text.get_width() // 2,
                start_button.centery - text.get_height() // 2
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if start_button.collidepoint(event.pos):
                    running = False
                    pygame.quit()

                if pygame.Rect(width_x - 12, 43, 24, 24).collidepoint(event.pos):
                    dragging_width = True

                if pygame.Rect(height_x - 12, 93, 24, 24).collidepoint(event.pos):
                    dragging_height = True

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_width = False
                dragging_height = False

            elif event.type == pygame.MOUSEMOTION:

                if dragging_width:
                    t = (mx - width_slider.x) / width_slider.w
                    width = max(1, min(60, round(1 + t * 59)))

                if dragging_height:
                    t = (mx - height_slider.x) / height_slider.w
                    height = max(1, min(60, round(1 + t * 59)))

    return width, height