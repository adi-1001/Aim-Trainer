import pygame
import math
import random
import time
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim training")

Target_increment = 300
Target_Event = pygame.USEREVENT 
Target_padding = 30
Top_bar_height = 50
BG_COLOR = (0, 25, 40)
font = pygame.font.SysFont("comicsans", 30)
Lives = 5
quit_button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 40)

DIFFICULTY_SETTINGS = {
    "easy": {"spawn_rate": 1000, "growth_rate": 0.25, "max_size": 40},
    "medium": {"spawn_rate": 600, "growth_rate": 0.3, "max_size": 30},
    "hard": {"spawn_rate": 400, "growth_rate": 0.35, "max_size": 25},
}


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECONDARY_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.growing = True
    
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.growing = False
        
        if self.growing:
            self.size += self.GROWTH_RATE
        
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (int(self.x), int(self.y)), int(self.size))
        pygame.draw.circle(win, self.SECONDARY_COLOR, (int(self.x), int(self.y)), int(self.size*0.8))
        pygame.draw.circle(win, self.COLOR, (int(self.x), int(self.y)), int(self.size*0.6))
        pygame.draw.circle(win, self.SECONDARY_COLOR, (int(self.x), int(self.y)), int(self.size*0.4))

    def collide(self, mouse_x, mouse_y):
        distance = math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)
        return distance <= self.size
    
def draw_window(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

    pygame.draw.rect(win, (0, 25, 40), quit_button_rect)
    quit_text = font.render("Quit", True, "white")
    win.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 8))
    
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1)) 
    minutes = int(secs // 60)

    return f"{minutes:02d} : {seconds:02d}.{milli}"

def draw_top_bar(win,elapsed_time,targets_press,misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH,Top_bar_height))
    time_label= font.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    speed = round(targets_press / elapsed_time, 2) if elapsed_time > 0 else 0
    speed_label = font.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = font.render(f"Hits: {targets_press}", 1, "black")
    lives_label = font.render(f"Lives: {Lives - (misses)}", 1, "black")

    win.blit(hits_label, (250, 5))
    win.blit(lives_label, (400, 5))
    win.blit(speed_label, (600, 5))
    win.blit(time_label, (5, 5))

def draw_home_screen(win):
    win.fill(BG_COLOR)
    title = font.render("Aim Trainer", 1, "white")
    instruct = font.render("Select Difficulty: [E]asy  [M]edium  [H]ard", 1, "white")

    win.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    win.blit(instruct, (WIDTH//2 - instruct.get_width()//2, 250))
    pygame.display.update()

    selected = None
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    selected = "easy"
                elif event.key == pygame.K_m:
                    selected = "medium"
                elif event.key == pygame.K_h:
                    selected = "hard"
    return selected


def end_screen( win, elapsed_time, targets_press, click):
    win.fill(BG_COLOR)
    time_label= font.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_press / elapsed_time, 2) if elapsed_time > 0 else 0
    speed_label = font.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = font.render(f"Hits: {targets_press}", 1, "white")
    accuracy = (targets_press / (targets_press + click)) * 100 if (targets_press + click) > 0 else 0
    accuracy_label = font.render(f"Accuracy: {accuracy:.2f}%", 1, "white")

    win.blit(hits_label, (get_middle(hits_label), 100))
    win.blit(accuracy_label, (get_middle(accuracy_label), 200))
    win.blit(speed_label, (get_middle(speed_label), 300))
    win.blit(time_label, (get_middle(time_label), 400))  



    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
    thank_you_screen(win)

        

def thank_you_screen(win):
    win.fill(BG_COLOR)
    big_font = pygame.font.SysFont("comicsans", 60, bold=True)
    small_font = pygame.font.SysFont("comicsans", 30)

    title = big_font.render("🎮 Thanks for Playing! 🎯", True, "white")
    tagline = small_font.render("Train hard, click fast, be legendary.", True, (0, 200, 200))
    exit_msg = small_font.render("Press any key or close window to exit.", True, "gray")

    win.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    win.blit(tagline, (WIDTH // 2 - tagline.get_width() // 2, 300))
    win.blit(exit_msg, (WIDTH // 2 - exit_msg.get_width() // 2, 400))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False


def get_middle(surface):
    return (WIDTH // 2 - surface.get_width() // 2)


def main():
    difficulty = draw_home_screen(WIN)
    settings = DIFFICULTY_SETTINGS[difficulty]

    Target.MAX_SIZE = settings["max_size"]
    Target.GROWTH_RATE = settings["growth_rate"]
    Target_increment = settings["spawn_rate"]
    quit_button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 40)


    run = True
    targets = []
    clock = pygame.time.Clock()
    click_total = 0
    targets_press = 0
    click = 0
    misses = 0
    Start_time = time.time()
    elapsed_time = 0

    pygame.time.set_timer(Target_Event, Target_increment)

    while run:
        clock.tick(60)
        elapsed_time = time.time() - Start_time
        click = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == Target_Event:
                x = random.randint(Target_padding, WIDTH - Target_padding)
                y = random.randint(Target_padding + Top_bar_height, HEIGHT - Target_padding)
                targets.append(Target(x, y))

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                click_total += 1
                if quit_button_rect.collidepoint(event.pos):
                    thank_you_screen(WIN)
                    run = False
                    break
                


        for target in targets[:]:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                misses += 1
            elif click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_press += 1
                break  

        if misses >= Lives:
            end_screen(WIN, elapsed_time, targets_press, click_total)
            run = False
            break

        draw_window(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_press, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
