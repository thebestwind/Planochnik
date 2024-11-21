class UserActions:
    def __init__(self):
        self.states = {}

    def set_state(self, user_id, key, value): #сохранить значение параметра тренировки для пользователя
        if user_id not in self.states:
            self.states[user_id] = {}
        self.states[user_id][key] = value

    def get_state(self, user_id, key): #получить значение параметра тренировки для пользователя
        return self.states.get(user_id, {}).get(key)

    def clear_state(self, user_id): #удалить все параметры тренировки для пользователя
        del self.states[user_id]

    def user_exists(self, user_id):
        return user_id in self.states

    def set_traning_param(self,user_id,number_of_drills,time_of_one_drill,number_of_rounds): #установить параметры тренировки для пользователя
        self.set_state(user_id, "number_of_drills", number_of_drills)
        self.set_state(user_id, "time_of_one_drill", time_of_one_drill)
        self.set_state(user_id, "number_of_rounds", number_of_rounds)

    def get_training_parameters(self, user_id): #получить параметры тренировки для пользователя
        number_of_drills = self.get_state(user_id, "number_of_drills")
        time_of_one_drill = self.get_state(user_id, "time_of_one_drill")
        number_of_rounds = self.get_state(user_id, "number_of_rounds")
        return number_of_drills, time_of_one_drill, number_of_rounds