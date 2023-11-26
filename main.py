# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

class PokemonInfoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.label = Label(text='Enter the name of a Pokémon:')
        self.text_input = TextInput(multiline=False)
        self.button = Button(text='Get Info', on_press=self.get_pokemon_info)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.button)

        return self.layout

    def get_pokemon_info(self, instance):
        pokemon_name = self.text_input.text

        # Make a request to the PokeAPI to get information about the Pokémon
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extract relevant information
            types = [t['type']['name'] for t in data['types']]
            strengths = []
            weaknesses = []
            vulnerabilities = []
            resistances = []

            for t in types:
                url_type = f"https://pokeapi.co/api/v2/type/{t}"
                type_data = requests.get(url_type).json()

                strengths.extend([s['name'] for s in type_data['damage_relations']['double_damage_to']])
                weaknesses.extend([w['name'] for w in type_data['damage_relations']['half_damage_to']])
                vulnerabilities.extend([v['name'] for v in type_data['damage_relations']['double_damage_from']])
                resistances.extend([r['name'] for r in type_data['damage_relations']['half_damage_from']])

            info_text = (
                f"\nPokemon: {pokemon_name.capitalize()}\n"
                f"Types: {', '.join(types)}\n"
                f"Strengths: {', '.join(strengths)}\n"
                f"Weaknesses: {', '.join(weaknesses)}\n"
                f"Vulnerabilities: {', '.join(vulnerabilities)}\n"
                f"Resistances: {', '.join(resistances)}\n"
            )

            # Display the information
            self.label.text = info_text
        else:
            self.label.text = f"Sorry, {pokemon_name} not found in the PokeAPI."

if __name__ == '__main__':
    PokemonInfoApp().run()
