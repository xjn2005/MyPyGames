import pygame
import json
import os
import sys

class Ranking:
    def __init__(self, settings):
        self.settings = settings
    
    def load(self):
        if not os.path.exists(self.settings.ranking_file):
            return []
        try:
            with open(self.settings.ranking_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def save(self, new_score, new_name):
        rankings = self.load()
        rankings.append({"name": new_name, "score": new_score})
        rankings = sorted(rankings, key=lambda x: -x["score"])[:self.settings.max_ranking]
        with open(self.settings.ranking_file, "w", encoding="utf-8") as f:
            json.dump(rankings, f, ensure_ascii=False, indent=2)
    
    def get_player_name(self, screen, font):
        name = ""
        input_active = True
        while input_active:
            screen.fill(self.settings.black)
            prompt_text = font.render("Enter your name (max 6 chars):", True, self.settings.white)
            prompt_rect = prompt_text.get_rect(center=(self.settings.total_screen_width//2, self.settings.screen_height//2 - 50))
            screen.blit(prompt_text, prompt_rect)
            name_text = font.render(name, True, self.settings.blue)
            name_rect = name_text.get_rect(center=(self.settings.total_screen_width//2, self.settings.screen_height//2))
            screen.blit(name_text, name_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 6 and event.unicode.isalnum():
                        name = name + event.unicode
            
            pygame.display.flip()
        return name.strip()
