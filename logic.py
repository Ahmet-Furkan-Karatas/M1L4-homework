import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}

    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.pokemon_type = None
        self.weight = None
        self.height = None
        self.abilities = None

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    self.name = data['forms'][0]['name']  # Pokémon'un adını ayarlama
                    self.pokemon_type = [type['type']['name'] for type in data['types']]  # Türleri alma
                    self.weight = data['weight']  # Ağırlığı alma
                    self.height = data['height']  # Boyu alma
                    self.abilities = [ability['ability']['name'] for ability in data['abilities']]  # Yetenekleri alma
                    return self.name  # Bir Pokémon'un adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"""
        Pokémonunuzun ismi: {self.name}
        Türü: {', '.join(self.pokemon_type)}
        Ağırlığı: {self.weight / 10} kg
        Boyu: {self.height / 10} m  
        Yetenekleri: {', '.join(self.abilities)}
        """  # Pokémon hakkında daha fazla bilgiyi içeren bir dize döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['sprites']['front_default']
                else:
                    return None  # İstek başarısız olursa döndürür
