import telebot
from emoji import emojize

member_countries_emojis = {
    'Antigua and Barbuda': emojize(":antigua_barbuda:", language='alias')+" (AG)",
    'Bahamas': emojize(":bahamas:", language='alias')+ " (BS)",
    'Barbados': emojize(":barbados:", language='alias')+" (BB)",
    'Belize': emojize(":belize:", language='alias')+ " (BZ)",
    'Canada': emojize(":canada:", language='alias')+ " (CA)", 
    'Dominica': emojize(":dominica:", language='alias')+ " (DM)",
    'Dominican Republic': emojize(":dominican_republic:", language='alias')+ " (DO)",
    'Grenada': emojize(":grenada:", language='alias')+ " (GD)",
    'Guyana': emojize(":guyana:", language='alias')+ " (GY)",
    'Jamaica': emojize(":jamaica:", language='alias')+ " (JM)",
    'Saint Kitts and Nevis': emojize(":st_kitts_nevis:", language='alias')+ " (KN)",
    'Saint Lucia': emojize(":st_lucia:", language='alias')+ " (LC)",
    'Saint Vincent and the Grenadines': emojize(":st_vincent_grenadines:", language='alias')+ " (VC)",
    'Suriname': emojize(":suriname:", language='alias')+ " (SR)",
    'Trinidad and Tobago': emojize(":trinidad_tobago:", language='alias')+ " (TT)",
    'USA': emojize(":us:", language='alias')+ " (US)",
    "Argentina": emojize(":argentina:", language='alias')+ " (AR)",
    "Bolivia": emojize(":bolivia:", language='alias')+ " (BO)",
    "Brazil": emojize(":brazil:", language='alias')+ " (BR)",
    "Chile": emojize(":chile:", language='alias')+ " (CL)",
    "Colombia": emojize(":colombia:", language='alias')+ " (CO)",
    "Costa Rica": emojize(":costa_rica:", language='alias')+ " (CR)",
    "Cuba": emojize(":cuba:", language='alias')+ " (CU)",
    "Ecuador": emojize(":ecuador:", language='alias')+ " (EC)",
    "El Salvador": emojize(":el_salvador:", language='alias')+ " (SV)",
    "Guatemala": emojize(":guatemala:", language='alias')+ " (GT)",
    "Haiti": emojize(":haiti:", language='alias')+ " (HT)",
    "Honduras": emojize(":honduras:", language='alias')+ " (HN)",
    "Mexico": emojize(":mexico:", language='alias')+ " (MX)",
    "Nicaragua": emojize(":nicaragua:", language='alias')+ " (NI)",
    "Panama": emojize(":panama:", language='alias')+ " (PA)",
    "Paraguay": emojize(":paraguay:", language='alias')+ " (PY)",
    "Peru": emojize(":peru:", language='alias')+ " (PE)",
    "Uruguay": emojize(":uruguay:", language='alias')+ " (UY)",
    "Venezuela": emojize(":venezuela:", language='alias')+ " (VE)",
    "Portugal": emojize(":portugal:", language='alias')+ " (PT)",
}

country_victims = [
    'Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 
    'Belize', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia',
    'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador',
    'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 
    'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 
    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'Suriname', 'Trinidad and Tobago', 'USA', 'Uruguay','Venezuela'
]

def emojize_countries(countries):
    emojis = []
    for country in countries:
        emojis.append(member_countries_emojis[country])
    return ', '.join(emojis)


def enviar_incidente(token, chat_id, title, content, category, url, countries, threat_actors):
    bot = telebot.TeleBot(token)
    texto = emojize(":police_car_light:", language='alias') + \
        " <b>Nuevo Incidente de "+category+"</b> " + emojize(":police_car_light: \n", language='alias') \
            + "<b>Title</b>: " + title + "\n"\
            + "<b>Threat Actors</b>: " + threat_actors + "\n"\
            + "<b>Content</b>: " + content \
            + "\n<b>Países miembros afectados</b>: " + emojize_countries(countries) \
            + " \n<b>Publicado en</b>: <a href=\"" + url + "\">Link</a>"
    for x in telebot.util.smart_split(texto, 4096):
        bot.send_message(chat_id, texto, parse_mode='HTML')
