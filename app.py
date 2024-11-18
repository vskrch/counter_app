import pygame
import sys
import sqlite3

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Counter App')

# Set up font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Initialize counter with seed value
seed = 3000
counter = seed

# Set up timer event
INCREMENT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(INCREMENT_EVENT, 2569)  # 3000 milliseconds = 3 seconds

# Set up SQLite database
conn = sqlite3.connect('counter.db') # Connect to database
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS counter (value INTEGER)''')
conn.commit()

def update_counter():
    global counter
    counter += 1

def save_counter():
    global counter, show_save_message, save_message_timer
    c.execute('DELETE FROM counter')
    c.execute('INSERT INTO counter (value) VALUES (?)', (counter,))
    conn.commit()
    show_save_message = True
    save_message_timer = pygame.time.get_ticks()

def load_counter():
    global counter
    c.execute('SELECT value FROM counter')
    row = c.fetchone()
    if row:
        counter = row[0]

def main():
    global counter, show_save_message, save_message_timer
    clock = pygame.time.Clock()

    # Load counter from database
    load_counter()

    # Set up buttons
    save_button = pygame.Rect(50, 250, 100, 40)
    end_button = pygame.Rect(250, 250, 100, 40)

    show_save_message = False
    save_message_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_counter()
                pygame.quit()
                sys.exit()
            elif event.type == INCREMENT_EVENT:
                update_counter()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if save_button.collidepoint(event.pos):
                    save_counter()
                elif end_button.collidepoint(event.pos):
                    save_counter()
                    pygame.quit()
                    sys.exit()

        # Clear screen
        screen.fill((0, 0, 0))

        # Render counter
        counter_text = font.render(str(counter), True, (255, 255, 255))
        text_rect = counter_text.get_rect(center=(width // 2, height // 2))
        screen.blit(counter_text, text_rect)

        # Render buttons
        pygame.draw.rect(screen, (0, 255, 0), save_button)
        pygame.draw.rect(screen, (255, 0, 0), end_button)
        save_text = small_font.render('Save', True, (0, 0, 0))
        end_text = small_font.render('End', True, (0, 0, 0))
        screen.blit(save_text, (save_button.x + 10, save_button.y + 5))
        screen.blit(end_text, (end_button.x + 10, end_button.y + 5))

        # Render save message
        if show_save_message:
            if pygame.time.get_ticks() - save_message_timer < 2000:  # Show for 2 seconds
                save_message = small_font.render('Progress Saved', True, (255, 255, 255))
                screen.blit(save_message, (width // 2 - save_message.get_width() // 2, height // 2 + 50))
            else:
                show_save_message = False

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

if __name__ == "__main__":
    main()