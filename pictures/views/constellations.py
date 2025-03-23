from django.shortcuts import render

def constellations_view(request):
    # Constellation data hardcoded
    constellations = [
        {"name": "Andromeda", "id": "and", "full_name": "Andromeda"},
        {"name": "Antlia", "id": "ant", "full_name": "Air Pump"},
        {"name": "Apus", "id": "aps", "full_name": "Bird of Paradise"},
        {"name": "Aquarius", "id": "aqr", "full_name": "Water Bearer"},
        {"name": "Aquila", "id": "aql", "full_name": "Eagle"},
        {"name": "Ara", "id": "ara", "full_name": "Altar"},
        {"name": "Aries", "id": "ari", "full_name": "Ram"},
        {"name": "Auriga", "id": "aur", "full_name": "Charioteer"},
        {"name": "Boötes", "id": "boo", "full_name": "Herdsman"},
        {"name": "Caelum", "id": "cae", "full_name": "Chisel"},
        {"name": "Camelopardalis", "id": "cam", "full_name": "Giraffe"},
        {"name": "Cancer", "id": "cnc", "full_name": "Crab"},
        {"name": "Canes Venatici", "id": "cvn", "full_name": "Hunting Dogs"},
        {"name": "Canis Major", "id": "cma", "full_name": "Great Dog"},
        {"name": "Canis Minor", "id": "cmi", "full_name": "Little Dog"},
        {"name": "Capricornus", "id": "cap", "full_name": "Sea Goat"},
        {"name": "Carina", "id": "car", "full_name": "Keel"},
        {"name": "Cassiopeia", "id": "cas", "full_name": "Cassiopeia"},
        {"name": "Centaurus", "id": "cen", "full_name": "Centaur"},
        {"name": "Cepheus", "id": "cep", "full_name": "Cepheus"},
        {"name": "Cetus", "id": "cet", "full_name": "Whale"},
        {"name": "Chamaeleon", "id": "cha", "full_name": "Chameleon"},
        {"name": "Circinus", "id": "cir", "full_name": "Compass"},
        {"name": "Columba", "id": "col", "full_name": "Dove"},
        {"name": "Coma Berenices", "id": "com", "full_name": "Berenice's Hair"},
        {"name": "Corona Australis", "id": "cra", "full_name": "Southern Crown"},
        {"name": "Corona Borealis", "id": "crb", "full_name": "Northern Crown"},
        {"name": "Corvus", "id": "crv", "full_name": "Crow"},
        {"name": "Crater", "id": "crt", "full_name": "Cup"},
        {"name": "Crux", "id": "cru", "full_name": "Southern Cross"},
        {"name": "Cygnus", "id": "cyg", "full_name": "Swan"},
        {"name": "Delphinus", "id": "del", "full_name": "Dolphin"},
        {"name": "Dorado", "id": "dor", "full_name": "Swordfish"},
        {"name": "Draco", "id": "dra", "full_name": "Dragon"},
        {"name": "Equuleus", "id": "equ", "full_name": "Little Horse"},
        {"name": "Eridanus", "id": "eri", "full_name": "River"},
        {"name": "Fornax", "id": "for", "full_name": "Furnace"},
        {"name": "Gemini", "id": "gem", "full_name": "Twins"},
        {"name": "Grus", "id": "gru", "full_name": "Crane"},
        {"name": "Hercules", "id": "her", "full_name": "Hercules"},
        {"name": "Horologium", "id": "hor", "full_name": "Clock"},
        {"name": "Hydra", "id": "hya", "full_name": "Water Snake"},
        {"name": "Hydrus", "id": "hyi", "full_name": "Water Snake"},
        {"name": "Indus", "id": "ind", "full_name": "Indian"},
        {"name": "Lacerta", "id": "lac", "full_name": "Lizard"},
        {"name": "Leo", "id": "leo", "full_name": "Lion"},
        {"name": "Leo Minor", "id": "lmi", "full_name": "Little Lion"},
        {"name": "Lepus", "id": "lep", "full_name": "Hare"},
        {"name": "Libra", "id": "lib", "full_name": "Scales"},
        {"name": "Lupus", "id": "lup", "full_name": "Wolf"},
        {"name": "Lynx", "id": "lyn", "full_name": "Lynx"},
        {"name": "Lyra", "id": "lyr", "full_name": "Lyre"},
        {"name": "Mensa", "id": "men", "full_name": "Table Mountain"},
        {"name": "Microscopium", "id": "mic", "full_name": "Microscope"},
        {"name": "Monoceros", "id": "mon", "full_name": "Unicorn"},
        {"name": "Musca", "id": "mus", "full_name": "Fly"},
        {"name": "Norma", "id": "nor", "full_name": "Square"},
        {"name": "Octans", "id": "oct", "full_name": "Octant"},
        {"name": "Ophiuchus", "id": "oph", "full_name": "Serpent Bearer"},
        {"name": "Orion", "id": "ori", "full_name": "Orion"},
        {"name": "Pavo", "id": "pav", "full_name": "Peacock"},
        {"name": "Pegasus", "id": "peg", "full_name": "Pegasus"},
        {"name": "Perseus", "id": "per", "full_name": "Perseus"},
        {"name": "Phoenix", "id": "phe", "full_name": "Phoenix"},
        {"name": "Pictor", "id": "pic", "full_name": "Easel"},
        {"name": "Pisces", "id": "psc", "full_name": "Fishes"},
        {"name": "Piscis Austrinus", "id": "psa", "full_name": "Southern Fish"},
        {"name": "Puppis", "id": "pup", "full_name": "Stern"},
        {"name": "Pyxis", "id": "pyx", "full_name": "Compass"},
        {"name": "Reticulum", "id": "ret", "full_name": "Reticle"},
        {"name": "Sagitta", "id": "sge", "full_name": "Arrow"},
        {"name": "Sagittarius", "id": "sgr", "full_name": "Archer"},
        {"name": "Scorpius", "id": "sco", "full_name": "Scorpion"},
        {"name": "Sculptor", "id": "scl", "full_name": "Sculptor"},
        {"name": "Scutum", "id": "sct", "full_name": "Shield"},
        {"name": "Serpens", "id": "ser", "full_name": "Serpent"},
        {"name": "Sextans", "id": "sex", "full_name": "Sextant"},
        {"name": "Taurus", "id": "tau", "full_name": "Bull"},
        {"name": "Telescopium", "id": "tel", "full_name": "Telescope"},
        {"name": "Triangulum", "id": "tri", "full_name": "Triangle"},
        {"name": "Triangulum Australe", "id": "tra", "full_name": "Southern Triangle"},
        {"name": "Tucana", "id": "tuc", "full_name": "Toucan"},
        {"name": "Ursa Major", "id": "uma", "full_name": "Great Bear"},
        {"name": "Ursa Minor", "id": "umi", "full_name": "Little Bear"},
        {"name": "Vela", "id": "vel", "full_name": "Sails"},
        {"name": "Virgo", "id": "vir", "full_name": "Virgin"},
        {"name": "Volans", "id": "vol", "full_name": "Flying Fish"},
        {"name": "Vulpecula", "id": "vul", "full_name": "Fox"}
    ]
    
    search_term = request.GET.get('search', '')
    
    if search_term:
        filtered_constellations = [
            c for c in constellations 
            if search_term.lower() in c['name'].lower() or 
               search_term.lower() in c['full_name'].lower()
        ]
    else:
        filtered_constellations = constellations
        
    context = {
        'constellations': filtered_constellations,
        'search_term': search_term
    }
    
    return render(request, 'constellations_list.html', context)