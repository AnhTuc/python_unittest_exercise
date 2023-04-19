class Player:
    def __init__(self,player_score = 60, name =None, receive_reward = 0):
        if name ==None :
            try:
                self.name = input("Enter player's name: ")
            except KeyboardInterrupt:
                self.name =''
        else:
            self.name = name
            
        self.score =player_score
        self.card = None
        self.tmp_reward = receive_reward
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        self._name = name

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self,score):
        self._score = score
    
    @property
    def card(self):
        return self._card

    @card.setter
    def card(self,assigned_card):
        self._card = assigned_card
    
    @property
    def tmp_reward(self):
        return self._tmp_reward

    @tmp_reward.setter
    def tmp_reward(self,receive_reward):
        self._tmp_reward = receive_reward

    


    