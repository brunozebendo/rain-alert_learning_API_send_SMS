"""A ideia do código é criar uma API que vai verificar o tempo nas próximas doze horas e
passar automaticamento um SMS caso vá chover. Se quiser colocar o código pra funcionar,
 pode-se usar o Python everywhere, site para rodar o código na hora programada"""
import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
"""abaixo o endereço da API, a chave obrigatória para essa API e as o espaço para as chaves obtidas no Twilio"""
"""abaixo, o environ siginifica que os códigos acima foram escondidos no enviroment, por
questão de segurança. Abaixo, vou explicar melhor."""

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")
"""abaixo estão os parâmetros dos dados que são requisitados pela API, assim como os que não queremos"""
weather_params = {
    "lat": "YOUR LATITUDE",
    "lon": "YOUR LONGITUDE",
    "appid": api_key,
    "exclude": "current,minutely,daily"
}
"""abaixo é usada a sintaxe para obter os dados no site, primeiro, o link que acima foi passado, depois
os parâmetros, depois, o raise for status, para caso dê um erro, então os dados obtidos são guardados
no weather_data como um dicionário json, então a variável weather_data guarda a variável weather_data mas
somente da chave da hora (hourly) com um slice de 12, ou seja, de 0 a 11"""

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
"""aqui a will rain é passada inicialmente como falsa para quando a condição for atingida 
ele fica verdadeira, isso foi feito para evitar que se passe o SMS doze vezes. A lógica do 
código é que o for loop verifique dentro do weather slice o campo id que, conforme a documentação da API
é o código que indica o tempo (sempre ler a documentação da API), assim, sempre que o id for menor que 700 significa
que está chovendo. Reparar como é obtido o dado dentro do dicionário json, passando a chave ["weather"], 
a localização do item [0] e uma outra chave ["id"]. Reparar como a informação é trabalhada, primeiro ela é
obtida de forma bruta na API, mas já trazendo só o que interessa ou é obrigatório, depois vai se reduzindo
até ficar apenas com o dado que se precisa"""
will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
"""já o código abaixo está indexado dentro do will_rain, ou seja, se o id estiver abaixo de 700, vai chover, e 
o resto do código é acionado, a sintaxe foi obtida do aplicativo Twilio, usado para enviar sms, o aplciativo
é pago"""
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
    print(message.status)
