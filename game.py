import pygame
from utils import WIDTH, HEIGHT, FPS, COLOURS, load_image, load_sound
from levels import PhishingIntroduction, Level1, Level2, Level3, PhishingInfo
from ui import Button

class GameStateManager:
    def __init__(self):
        self.state = "HOME_SCREEN"

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state

class Game:
    def __init__(self):
        print("Initialising game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fonolt")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.current_level = None
        self.current_level_number = 0
        self.state_manager = GameStateManager()
        self.load_assets()
        self.font = pygame.font.SysFont('Comic Sans MS', 36)

    def load_assets(self):
        print("Loading assets")
        self.background = load_image('background.png', (WIDTH, HEIGHT))
        self.click_sound = load_sound('click.mp3')
        self.correct_sound = load_sound('correct.mp3')
        self.wrong_sound = load_sound('wrong.mp3')
        self.home_music = load_sound('home_music.mp3')
        self.intro_music = load_sound('level1music.mp3')

    def run(self):
        print("Running game")
        while True:
            if self.state_manager.get_state() == "HOME_SCREEN":
                self.show_home_screen()
            elif self.state_manager.get_state() == "PLAYING":
                self.run_levels()
            elif self.state_manager.get_state() == "END_SCREEN":
                self.show_end_screen()
                break

    def show_home_screen(self):
        print("Showing home screen")
        self.home_music.play(-1)  # Play home screen music
        startButton = Button("Start", WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
        exitButton = Button("Exit", WIDTH // 2 - 50, HEIGHT // 2 + 70, 100, 50)

        while self.state_manager.get_state() == "HOME_SCREEN":
            self.screen.blit(self.background, (0, 0))
            startButton.draw(self.screen)
            exitButton.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startButton.is_clicked(event.pos):
                        print("Start button clicked")
                        self.home_music.stop()
                        self.intro_music.play(-1)  # Play intro music
                        self.state_manager.set_state("PLAYING")
                        return
                    elif exitButton.is_clicked(event.pos):
                        print("Exit button clicked")
                        pygame.quit()
                        quit()

            self.clock.tick(FPS)

    def run_levels(self):
        print("Running levels")
        levels = [
            PhishingIntroduction(self),
            Level1(self),
            Level2(self),
            Level3(self),
        ]

        for level in levels:
            self.current_level = level
            print(f"Running level: {level.__class__.__name__}")
           # if isinstance(level, Level1):
               # self.intro_music.stop()  # Stop intro music before Level1 starts
            level_score = level.run()
            if level_score is not None:
                self.score += level_score
            if not isinstance(level, PhishingIntroduction) and not isinstance(level, PhishingInfo):
                self.show_level_complete()
                self.current_level_number += 1  # Increment after showing level complete

        self.state_manager.set_state("END_SCREEN")

    def show_end_screen(self):
        print("Showing end screen")
        self.screen.fill(COLOURS['WHITE'])
        self.render_text("Congratulations!", COLOURS['BLACK'], (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        self.render_text("You've successfully completed the Phishing Awareness Game.", COLOURS['BLACK'], (WIDTH // 2 - 300, HEIGHT // 2))
        self.render_text("Well done for passing!", COLOURS['BLACK'], (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        pygame.display.flip()
        pygame.time.wait(5000)

    def render_text(self, text, color, position):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def show_level_complete(self):
        self.screen.fill(COLOURS['WHITE'])
        self.render_text(f"Level {self.current_level_number + 1} Complete!", COLOURS['BLACK'], (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        self.render_text(f"Current Score: {self.score}", COLOURS['BLACK'], (WIDTH // 2 - 100, HEIGHT // 2))
        self.render_text("Press any key to continue", COLOURS['BLACK'], (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    waiting = False
            self.clock.tick(FPS)