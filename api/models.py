from django.db import models
from django.utils import timezone
from . import main

class Game(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=main.N_POSITIONS, default=main.START_STATE)

    def __str__(self):
        return main.neat(self.state)
    
    def move(self, i = None):
        if self.end is not None:
            return False
        if i is None or i == {}:
            i = main.smart_move(self.state)
        if not isinstance(i, int):
            return False
        try:
            self.state = main.move(self.state, i)
        except:
            return False
        if main.get_result(self.state):
            self.end = timezone.now()
        self.save()
        return True


        
    