name="hashMap"

class HashMap:


    def __init__(self, array_size):
        self.array_size = array_size
        self.array = [None for item in range(array_size)]

    def hasher(self, key, count_collisions=0):
        key_bytes = key.encode()
        hasher_code = sum(key_bytes)
        return hasher_code + count_collisions

    def array_index_compute(self, hasher_code):
        return hasher_code % self.array_size

    def key_after_collision(self, key, number_collisions=1):
        new_hasher_code = self.hasher(key, number_collisions)
        new_array_index = self.array_index_compute(new_hasher_code)
        return new_array_index


    def assign(self, key, value):
        array_index = self.array_index_compute(self.hasher(key))
        current_array_value = self.array[array_index]

        if current_array_value is None:
            self.array[array_index] = [key, value]
            return

        if current_array_value[0] == key:
          self.array[array_index] = [key, value]
          return

        # Collision!
        number_collisions = 1

        while(current_array_value[0] != key):
            new_array_index = self.key_after_collision(key, number_collisions)
            current_array_value = self.array[new_array_index]

            if current_array_value is None:
                self.array[new_array_index] = [key, value]
                return

            if current_array_value[0] == key:
                self.array[new_array_index] = [key, value]
                return

            number_collisions += 1
            if(number_collisions>self.array_size):
                print("Array Full")
                return

        return

    def retrieve(self, key):
        array_index = self.array_index_compute(self.hasher(key))
        tentative_return_value = self.array[array_index]

        if tentative_return_value is None:
          return None

        if tentative_return_value[0] == key:
          return tentative_return_value[1]

        collision_count_retrieve = 1

        while (tentative_return_value != key):
          retrieving_array_index = self.key_after_collision(key, collision_count_retrieve)
          tentative_return_value = self.array[retrieving_array_index]

          if tentative_return_value is None:
            return None

          if tentative_return_value[0] == key:
            return tentative_return_value[1]

          collision_count_retrieve += 1

          return
