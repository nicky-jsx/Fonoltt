import pygame
import random
from utils import WIDTH, HEIGHT, COLOURS, TIMER, load_links_from_csv, load_image, load_sound
from ui import Button, position_text
import time

class BaseLevel:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

    def show_instructions(self, instructions):
        print("Showing instructions")
        self.game.screen.blit(self.game.background, (0, 0))
        y = 100
        for line in instructions:
            self.game.render_text(line, COLOURS['WHITE'], (50, y))
            y += 40
        continue_button = Button("Continue", WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
        continue_button.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting game from instructions")
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        print("Continue button clicked")
                        return

    def show_tutorial(self, tutorial):
        print("Showing tutorial")
        self.game.screen.blit(self.game.background, (0, 0))
        y = 100
        for line in tutorial:
            self.game.render_text(line, COLOURS['WHITE'], (50, y))
            y += 40
        continue_button = Button("Continue", WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
        continue_button.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting game from tutorial")
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        print("Continue button clicked")
                        return

    def play_scenario(self, scenarios, question, options, time_limit=TIMER):
        print("Playing scenario")
        score = 0
        total_scenarios = len(scenarios)

        for scenario in scenarios:
            start_time = pygame.time.get_ticks()
            result = None

            while True:
                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
                remaining_time = max(0, time_limit - elapsed_time)

                self.game.screen.blit(self.game.background, (0, 0))

                # Render email content
                y = 50
                for line in scenario['content']:
                    self.game.render_text(line, COLOURS['WHITE'], (50, y))
                    y += 30

                # Render question and other information
                self.game.render_text(question, COLOURS['WHITE'], (50, y + 20))
                self.game.render_text(f"Time left: {int(remaining_time)}s", COLOURS['WHITE'], (WIDTH - 150, 20))
                self.game.render_text(f"Score: {score}/{total_scenarios}", COLOURS['WHITE'], (WIDTH - 150, 50))

                # Render buttons
                buttons = [Button(option, 50 + i*150, HEIGHT - 100, 100, 50) for i, option in enumerate(options)]
                for button in buttons:
                    button.draw(self.game.screen)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, button in enumerate(buttons):
                            if button.is_clicked(event.pos):
                                result = "Correct" if scenario['is_legit'] == (options[i] == "Legitimate") else "Incorrect"
                                print(f"Button clicked: {options[i]}, Result: {result}")
                                if result == "Correct":
                                    score += 1
                                    self.game.correct_sound.play()
                                else:
                                    self.game.wrong_sound.play()
                                self.show_feedback(result, scenario.get('explanation', 'No explanation provided.'))
                                break
                if result:
                    break

                if remaining_time <= 0:
                    print("Time's up")
                    self.show_feedback("Time's up", scenario.get('explanation', 'No explanation provided.'))
                    break

            self.game.clock.tick(60)

        return score

    def show_feedback(self, result, explanation):
        print(f"Showing feedback: {result}, Explanation: {explanation}")
        self.game.screen.fill(COLOURS['BLACK'])
        self.game.render_text(result, COLOURS['WHITE'], (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        self.game.render_text(explanation, COLOURS['WHITE'], (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def show_result(self, result):
        self.game.screen.fill(COLOURS['BLACK'])
        self.game.render_text(result, COLOURS['WHITE'], (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        raise NotImplementedError


class PhishingIntroduction(BaseLevel):
    def run(self):
        instructions = [
            "Welcome to the Phishing Awareness Game!",
            "In this game, you will learn how to identify phishing emails.",
            "Each level will present you with different scenarios.",
            "You'll need to analyse the content and make quick decisions.",
            "Remember, accuracy is key in spotting phishing attempts!",
            "As you progress, the challenges will become more sophisticated.",
            "Good luck and stay vigilant!"
        ]

        self.show_dynamic_instructions(instructions)

    def show_dynamic_instructions(self, instructions):
        self.game.screen.blit(self.game.background, (0, 0))
        pygame.display.flip()

        font = pygame.font.Font(None, 32)
        text_color = COLOURS['WHITE']
        y_position = 100
        line_height = 40

        for line in instructions:
            for i in range(len(line) + 1):
                self.game.screen.blit(self.game.background, (0, 0))

                # Render all previous lines
                for j, prev_line in enumerate(instructions[:instructions.index(line)]):
                    text_surface = font.render(prev_line, True, text_color)
                    self.game.screen.blit(text_surface, (50, 100 + j * line_height))

                # Render current line
                current_text = line[:i]
                text_surface = font.render(current_text, True, text_color)
                self.game.screen.blit(text_surface, (50, y_position))

                pygame.display.flip()
                time.sleep(0.02)  # Adjust this value to change the text speed

            y_position += line_height
            time.sleep(0.5)  # Pause between lines

        continue_button = Button("Continue", WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
        continue_button.draw(self.game.screen)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        waiting = False

        self.game.click_sound.play()

class Level1(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.links = load_links_from_csv('links.csv')
        self.background = load_image('background.png', (WIDTH, HEIGHT))
        self.gameplay_music = load_sound('level1_music.mp3')

    def run(self):
        instructions = [
            "Level 1: Identifying Legitimate Links",
            "Click on legitimate links and avoid phishing links.",
            "Links will fall from the top of the screen.",
            "Score points for correct choices, lose points for mistakes.",
            "Reach 15 points to pass, game over at -5 points."
        ]
        tutorial = [
            ("Welcome to the Phishing Awareness Game!", "In this tutorial, we'll guide you through some key strategies to identify phishing attacks and stay safe online."),
            ("Understanding Phishing", "Phishing is a type of cyberattack where attackers impersonate legitimate entities to trick you into revealing sensitive information. Malicious actors can contact you through anything that has a messaging function, however in this game we will focus on emails. Click next to see how you can recognise a phishing attack."),
            ("Check for HTTPS", "Attackers can attach links to emails and prompt you to click on them. If clicked on, malware could be installed onto your device and disrupt your system, leaving you no control over it. In other cases, you'll be redirected to another website and further prompted to submit your personal details. If submitted, attackers will exploit this data and use it to their advantage. This could lead to identity theft, financial loss, bad reputation, etc. Ensure links start with 'https'. This indicates secure communication, but remember some phishing sites may also use HTTPS. So look for other factors too."),
            ("Beware of Shortened URLs", "Phishing links often use URL shorteners to hide their true destination. Be cautious with shortened URLs from unknown sources. E.g. https://bit.ly/3nQW4t (Phishing - URL shortener used)"),
            ("Look for Misspellings", "Phishing links often have subtle misspellings in the URL. For example:\n\n1. https://www.google.com (Legitimate)\n2. http://www.go0gle.com (Phishing - Notice the '0' instead of 'o')"),
            ("Identify Numbers in Links", "While legitimate sites may use numbers in their URLs, be cautious if the numbers seem random or unnecessary, as this can sometimes indicate a phishing attempt.\n\n1. https://www.3skyscanner123.co.uk (Phishing - Notice the random numbers)\n2. https://www.skyscanner.net/hotels/search?entity_id=27545988&checkin=2024-07-28&checkout=2024-07-29&adults=2&rooms=1 (Legitimate)"),
            ("Unknown Senders", "Be wary of links sent from unknown senders or unexpected messages from known contacts."),
            ("Hover Over Links", "Hover over links to see the actual URL before clicking. Ensure it matches the legitimate source."),
            ("Check Domain Extensions", "Sometimes phishing links use domain extensions that are less common or mimic legitimate extensions. E.g. http://www.bankofamerica.happy. Reputable companies typically use well-known domain extensions like .com, .org, or country-specific ones like .co.uk. Extensions such as .happy are unusual and unlikely to be used by legitimate businesses"),
            ("Good luck!", "Each level will present you with different scenarios. Stay alert and apply what you've learned!")
        ]

        self.show_tutorial(tutorial)
        self.show_instructions(instructions)

        while True:
            result = self.play_falling_links()
            self.gameplay_music.stop()
            if result:
                return True  # Level passed
            else:
                self.show_result("Level Failed. Try again!")
                pygame.time.wait(2000)

    def show_tutorial(self, tutorial):
        current_slide = 0
        while current_slide < len(tutorial):
            title, content = tutorial[current_slide]
            self.game.screen.blit(self.background, (0, 0))

            font_title = pygame.font.Font(None, 36)
            font_content = pygame.font.Font(None, 24)
            text_color = COLOURS['WHITE']

            # Render title
            title_surface = font_title.render(title, True, text_color)
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
            self.game.screen.blit(title_surface, title_rect)

            # Render content
            words = content.split()
            lines = []
            current_line = []
            for word in words:
                test_line = current_line + [word]
                test_width = font_content.size(' '.join(test_line))[0]
                if test_width <= WIDTH - 100:  # 100 is the total left and right margin
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))

            y_position = 100
            for line in lines:
                text_surface = font_content.render(line, True, text_color)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y_position))
                self.game.screen.blit(text_surface, text_rect)
                y_position += 30

            # Add Previous and Next buttons
            next_button = Button("Next", WIDTH - 150, HEIGHT - 70, 100, 50)
            next_button.draw(self.game.screen)

            if current_slide > 0:
                prev_button = Button("Previous", 50, HEIGHT - 70, 100, 50)
                prev_button.draw(self.game.screen)

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if next_button.is_clicked(event.pos):
                            waiting = False
                            current_slide += 1
                            self.game.click_sound.play()
                        elif current_slide > 0 and prev_button.is_clicked(event.pos):
                            waiting = False
                            current_slide -= 1
                            self.game.click_sound.play()

        # After the tutorial is complete, show a "Start Game" button
        self.game.screen.blit(self.background, (0, 0))
        self.game.render_text("Tutorial Complete!", COLOURS['WHITE'], (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        start_button = Button("Start Game", WIDTH // 2 - 80, HEIGHT - 70, 150, 50)
        start_button.draw(self.game.screen)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event.pos):
                        waiting = False
                        self.game.click_sound.play()

    def show_instructions(self, instructions):
        self.game.screen.blit(self.background, (0, 0))

        font_title = pygame.font.Font(None, 48)  # Larger font for the title
        font_instructions = pygame.font.Font(None, 32)  # Smaller font for instructions
        text_color = COLOURS['WHITE']

        # Render title
        title_surface = font_title.render(instructions[0], True, text_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        self.game.screen.blit(title_surface, title_rect)

        # Render instructions
        y_position = 120
        for instruction in instructions[1:]:
            wrapped_lines = position_text(instruction, font_instructions, WIDTH - 100)
            for line in wrapped_lines:
                text_surface = font_instructions.render(line, True, text_color)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y_position))
                self.game.screen.blit(text_surface, text_rect)
                y_position += 40  # Adjust vertical spacing between lines

        continue_button = Button("Continue", WIDTH // 2 - 50, HEIGHT - 70, 100, 50)
        continue_button.draw(self.game.screen)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        waiting = False
                        self.game.click_sound.play()


    def play_falling_links(self):
        score = 0
        base_speed = 2
        speed_increment = 0.1
        current_speed = base_speed
        falling_links = []

        start_time = pygame.time.get_ticks()



        while True:
            self.game.screen.blit(self.background, (0, 0))
            self.game.render_text(f"Score: {score}", COLOURS['WHITE'], (WIDTH - 150, 20))

            amount_of_time = (pygame.time.get_ticks() - start_time) / 1000
            current_speed = base_speed + (amount_of_time // 10) * speed_increment

            if random.randint(1, 30) == 1 and len(falling_links) < 5:
                link = random.choice(self.links)
                new_link = {
                    'text': link['text'],
                    'is_legit': link['is_legit'],
                    'x': random.randint(0, WIDTH - 200),
                    'y': 0
                }
                if not self.check_collision(new_link,falling_links):
                    falling_links.append(new_link)

            for link in falling_links:
                link['y'] += current_speed
                text_surface = self.game.font.render(link['text'], True, COLOURS['WHITE'])
                text_rect = text_surface.get_rect(center=(link['x'], link['y']))
                if text_rect.left < 0:
                    text_rect.left = 0
                elif text_rect.right > WIDTH:
                    text_rect.right = WIDTH
                link['rect'] = text_rect  # Store the rect for click detection
                self.game.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for link in falling_links:
                        if link['rect'].collidepoint(mouse_pos):
                            if link['is_legit']:
                                score += 1
                                self.game.correct_sound.play()
                            else:
                                score -= 1
                                self.game.wrong_sound.play()
                            falling_links.remove(link)
                            break

            falling_links = [link for link in falling_links if link['y'] < HEIGHT]

            if score >= 15:
                self.show_result("Level Completed!")
                return True
            elif score <= -5:
                self.show_result("Level Failed")
                return False

            self.game.clock.tick(60)  # Limit the frame rate to 60 FPS

    def check_collision(self,new_link,falling_links):
            for link in falling_links:
                if abs(new_link['x'] - link['x']) < 200 and abs(new_link['y'] - link['y']) < 50:
                    return True
            return False

class Level2(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('level2.png', (WIDTH, HEIGHT))
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def run(self):
        instructions = [
            "Level 2: Identifying Phishing Emails",
            "Analyse emails to determine if they're legitimate or phishing attempts.",
            "You have 30 seconds for each decision.",
            "Be cautious of unusual requests and sender addresses."
        ]
        scenarios = [
            {
                "content": ["From: admin@universityy-portal.com",
                            "Subject: Urgent: Update Your Student Login",
                            "Body: Dear Student,",
                            "Our system requires you to update your login credentials immediately.",
                            "Click here to update your username and password: http://uni-edef.0239234-upd34ate.com"],
                "is_legit": False,
                "explanation": "This is a phishing attempt. The university wouldn't ask you to update credentials through an external link. Always go directly to the official university website."
            },
            {
                "content": ["From: library@fonolt.ac,uk",
                            "Subject: Library Account Overdue Notice",
                            "Body: Dear Student,",
                            "You have overdue items. To avoid fines, please return them or renew online.",
                            "Log in to your library account on the university's website to renew them."],
                "is_legit": True,
                "explanation": "This email is likely legitimate. It's from an official university email address and directs you to the official university library website."
            },
            {
                "content": ["From: financial.aid@Fomyolt.com",
                            "Subject: Immediate Action Required - Reduced Tuition Fees",
                            "Body: Congrats! We have reduced you tuition fees.",
                            "please confirm your bank details by replying to this email."],
                "is_legit": False,
                "explanation": "This is a phishing attempt. The university would never ask for bank details via email. Financial aid communications typically come from official .ac.uk addresses. The sender also uses very informal language."
            },
            {
                "content": ["From: career.services@fonolt.ac.uk",
                            "Subject: Exclusive Job Opportunity for Students",
                            "Body: A local company is offering part-time positions for our students.",
                            "If interested, submit your resume through our secure portal:"],
                "is_legit": True,
                "explanation": "This email is likely legitimate. It's from an official university email and directs you to the university's secure career portal."
            },
            {
                "content": ["From: IT-support@university-helpdesk.net",
                            "Subject: Critical Security Update Required",
                            "Body: To protect your student account from recent cyber attacks,",
                            "click below to download and install this security patch immediately:",
                            "[Download Security Patch]"],
                "is_legit": False,
                "explanation": "This is a phishing attempt. University IT departments don't send security patches via email. Updates are typically done through official channels or on campus."
            }
        ]

        while True:
            self.show_instructions(instructions)
            score = self.play_scenario(scenarios, "Is this email legitimate or phishing?", ["Legitimate", "Phishing"], time_limit=30)
            if score >= 5:  # Passing score is 3 out of 5
                self.show_result("Level Completed!")
                return True
            else:
                self.show_result("Level Failed. Try again!")
                pygame.time.wait(2000)


    def render_text(self, text, x, y, font=None, color=COLOURS['BLACK']):
        if font is None:
            font = self.font_small
        text_surface = font.render(text, True, color)
        self.game.screen.blit(text_surface, (x, y))

    def render_multiline_text(self, lines, start_x, start_y, line_height=30):
        for i, line in enumerate(lines):
            self.render_text(line, start_x, start_y + i * line_height)

    def show_instructions(self, instructions):
            self.game.screen.blit(self.background, (0, 0))

            font_title = pygame.font.Font(None, 48)  # Larger font for the title
            font_instructions = pygame.font.Font(None, 32)  # Smaller font for instructions
            text_color = COLOURS['BLACK']

            # Render title
            title_surface = font_title.render(instructions[0], True, text_color)
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
            self.game.screen.blit(title_surface, title_rect)

            # Render instructions
            y_position = 120
            for instruction in instructions[1:]:
                wrapped_lines = position_text(instruction, font_instructions, WIDTH - 100)
                for line in wrapped_lines:
                    text_surface = font_instructions.render(line, True, text_color)
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_position))
                    self.game.screen.blit(text_surface, text_rect)
                    y_position += 40  # Adjust vertical spacing between lines

            continue_button = Button("Continue", WIDTH // 2 - 50, HEIGHT - 70, 100, 50)
            continue_button.draw(self.game.screen)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if continue_button.is_clicked(event.pos):
                            waiting = False
                            self.game.click_sound.play()


    def play_scenario(self, scenarios, question, options, time_limit):
        score = 0
        for scenario in scenarios:
            start_time = pygame.time.get_ticks()
            result = None

            while True:
                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
                remaining_time = max(0, time_limit - elapsed_time)

                self.game.screen.blit(self.background, (0, 0))

                # Render email content
                self.render_multiline_text(scenario['content'], 50, 50)

                # Render question and other information
                self.render_text(question, 50, HEIGHT - 150, self.font_large)
                self.render_text(f"Time left: {int(remaining_time)}s", WIDTH - 200, 20, self.font_small)
                self.render_text(f"Score: {score}/{len(scenarios)}", WIDTH - 200, 50, self.font_small)

                # Render buttons
                buttons = [
                    Button(options[0], WIDTH // 2 - 130, HEIGHT - 70, 120, 50),
                    Button(options[1], WIDTH // 2 + 10, HEIGHT - 70, 120, 50)
                ]
                for button in buttons:
                    button.draw(self.game.screen)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, button in enumerate(buttons):
                            if button.is_clicked(event.pos):
                                result = "Correct" if scenario['is_legit'] == (options[i] == "Legitimate") else "Incorrect"
                                if result == "Correct":
                                    score += 1
                                    self.game.correct_sound.play()
                                else:
                                    self.game.wrong_sound.play()
                                self.show_feedback(result, scenario['explanation'])
                                break
                if result:
                    break

                if remaining_time <= 0:
                    self.show_feedback("Time's up", scenario['explanation'])
                    break

            self.game.clock.tick(60)

        return score

    def show_feedback(self, result, explanation):
        self.game.screen.blit(self.background, (0, 0))
        self.render_text(result, 50, 50, self.font_large)
        wrapped_explanation = self.wrap_text(explanation, 60)
        self.render_multiline_text(wrapped_explanation, 50, 100)
        pygame.display.flip()
        pygame.time.wait(3000)

    def wrap_text(self, text, max_chars_per_line):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            if len(' '.join(current_line + [word])) <= max_chars_per_line:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

class Level3(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('level3.png', (WIDTH, HEIGHT))
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def run(self):
        instructions = [
            "Level 3: Advanced Phishing Detection",
            "Analyse emails to determine if they're legitimate or phishing attempts.",
            "You have 20 seconds for each decision.",
            "Look for unusual sender addresses and requests for sensitive information."
        ]
        self.show_instructions(instructions)
        scenarios = [
            {
                "content": ["From: professor.smith@gmail.com",
                            "Subject: Urgent: Course Materials Update",
                            "Body: Dear Student,",
                            "I've updated the course materials for next week.",
                            "Please download them from this shared drive: https://drive.go000gleeee/course-materials",
                            "Use your university email to access."],
                "is_legit": False,
                "explanation": "This is a sophisticated phishing attempt. While it appears to be from a professor, the email domain is not the official university domain. Also, legitimate course materials are typically shared through the university's learning management system, not external drives."
            },
            {
                "content": ["From: alumni@fonolt.ac.uk",
                            "Subject: Exclusive Alumni Network Pre-Registration",
                            "Body: As a current student, you're eligible for early access to our Alumni Network.",
                            "Register now to connect with successful graduates in your field!",
                            "https://alumni.fonolt.ac.uk/network-signup"],
                "is_legit": True,
                "explanation": "This email is legitimate. It's from an official university email address and the link points to the university's domain. Pre-registration for alumni networks is a common practice in universities. 'ac.uk' is also a common TLD for universities."
            },
            {
                "content": ["From: study.abroad@youruni.com",
                            "Subject: Last Chance!!: Study Abroad Scholarship",
                            "Body: Dear Student,",
                            "You've been selcted for a last-minute study abroad sch0larship!",
                            "To claim it, we need your passport details and a £100 processing fee.",
                            "Reply with the information now and well send payment instructions!!"],
                "is_legit": False,
                "explanation": "This is a phishing attempt. While the email appears to be from a legitimate university address, asking for passport details and a processing fee via email is not standard practice for scholarship applications. Also notice the spelling and grammar mistakes."
            },
            {
                "content": ["From: graduation.team@fonolt.ac,uk",
                            "Subject: Action Required: Degree Classification Update",
                            "Body: Our records show you're approaching graduation.",
                            "Please review your degree award and confirm on the student portal",
                            "Ensure all information is correct to avoid graduation delays."],
                "is_legit": True,
                "explanation": "This email is legitimate. It's an official Fonolt University email and directs you to the university's website."
            },
            {
                "content": ["From: campus.security@uni-alrt@gmail.com",
                            "Subject: URGENT: Campus Security Protocol Update",
                            "Body: Due to recent incidents, we're updating our security protocols.",
                            "All students must verify their ID and emergency contacts immediately.",
                            "Update your information here: https://uni-security-update.org"],
                "is_legit": False,
                "explanation": "This is a phishing attempt. While the subject seems urgent, the email is not from the official university domain. Legitimate security updates would be communicated through official university channels and would direct you to their official website."
            },
            {
                "content": ["From: ella.jones.grant@fonolot.ac.uk",
                            "Subject: Undergraduate Research Grant Opportunity",
                            "Body: Congratulations! As you acheived a first class hounours this year, you are eligible for our undergraduate research grant.",
                            "Submit your proposal through the academic portal:",
                            "Deadline: Next Friday, 5 PM."],
                "is_legit": True,
                "explanation": "This email is legitimate. It's from an official university email address and directs to the university's research portal. Grant opportunities are common in universities."
            },
            {
                "content": ["From: IT.support@outlook.com",
                            "Subject: Critical: Multi-Factor Authentication Update",
                            "Body: We're enhancing our security measures.",
                            "To continue accessing university services, click here to set up MFA:",
                            "http://security.uni-for-you.hap/mfa-setup",
                            "This process requires your university login credentials.",
                            "If you do not update this, you are lose access to accountt."],
                "is_legit": False,
                "explanation": "This is a sophisticated phishing attempt. While the email appears to be from IT support, the link doesn't lead to the official university domain. The email also contains spelling mistakes and urgently requests you to click the link."
            },
            {
                "content": ["From: parking@fonolt.ac.uk",
                            "Subject: New Smart Parking System - Registration Required",
                            "Body: We're upgrading to a smart parking system for all campus lots.",
                            "Register your vehicle and select your preferred payment method on the university's website.",
                            "Note: A one-time £5 registration fee applies."],
                "is_legit": True,
                "explanation": "This email is legitimate. It's from an official university email and directs you to the university's parking services page."
            }
        ]
        score = self.play_scenario(scenarios, "Is this email legitimate or phishing?", ["Legitimate", "Phishing"], time_limit=20)
        return score

    def render_text(self, text, x, y, font=None, color=COLOURS['WHITE']):
        if font is None:
            font = self.font_small
        text_surface = font.render(text, True, color)
        self.game.screen.blit(text_surface, (x, y))

    def render_multiline_text(self, lines, start_x, start_y, line_height=30):
        for i, line in enumerate(lines):
            self.render_text(line, start_x, start_y + i * line_height)

    def show_instructions(self, instructions):
        self.game.screen.blit(self.background, (0, 0))
        self.render_multiline_text(instructions, 50, 50)
        continue_button = Button("Continue", WIDTH // 2 - 50, HEIGHT - 70, 100, 50)
        continue_button.draw(self.game.screen)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        waiting = False
                        self.game.click_sound.play()

    def play_scenario(self, scenarios, question, options, time_limit):
        score = 0
        for scenario in scenarios:
            start_time = pygame.time.get_ticks()
            result = None

            while True:
                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
                remaining_time = max(0, time_limit - elapsed_time)

                self.game.screen.blit(self.background, (0, 0))

                # Render email content
                self.render_multiline_text(scenario['content'], 50, 50)

                # Render question and other information
                self.render_text(question, 50, HEIGHT - 150, self.font_large)
                self.render_text(f"Time left: {int(remaining_time)}s", WIDTH - 200, 20, self.font_small)
                self.render_text(f"Score: {score}/{len(scenarios)}", WIDTH - 200, 50, self.font_small)

                # Render buttons
                buttons = [
                    Button(options[0], WIDTH // 2 - 130, HEIGHT - 70, 120, 50),
                    Button(options[1], WIDTH // 2 + 10, HEIGHT - 70, 120, 50)
                ]
                for button in buttons:
                    button.draw(self.game.screen)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, button in enumerate(buttons):
                            if button.is_clicked(event.pos):
                                result = "Correct" if scenario['is_legit'] == (options[i] == "Legitimate") else "Incorrect"
                                if result == "Correct":
                                    score += 1
                                    self.game.correct_sound.play()
                                else:
                                    self.game.wrong_sound.play()
                                self.show_feedback(result, scenario['explanation'])
                                break
                if result:
                    break

                if remaining_time <= 0:
                    self.show_feedback("Time's up", scenario['explanation'])
                    break

            self.game.clock.tick(60)

        return score


class PhishingInfo(BaseLevel):
    def __init__(self, game, info):
        super().__init__(game)
        self.info = info

    def run(self):
        self.show_instructions(self.info)
