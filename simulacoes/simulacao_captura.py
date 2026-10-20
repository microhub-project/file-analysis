import csv
import random
import time

servidores = [
    {"instancia":"instancia_01","microsservico":"microsservico_01"},
    {"instancia":"instancia_01","microsservico":"microsservico_02"},
    {"instancia":"instancia_02","microsservico":"microsservico_03"},
    {"instancia":"instancia_02","microsservico":"microsservico_04"},
    {"instancia":"instancia_03","microsservico":"microsservico_05"},
    {"instancia":"instancia_03","microsservico":"microsservico_06"}
]

def capture():
    disco_inicial = 200.0

    with open("simulacao_ano_v2.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([
            'nome_instancia',
            'nome_microsservico',
            'porcentagem_cpu',
            'frequencia_cpu',
            'porcentagem_ram',
            'porcentagem_mem_swap',
            'qtd_processos',
            'qtd_zumbis',
            'bytes_upload',
            'bytes_download',
            'disco',
            'data_hora',
            'valor_estimado'
        ])
    for j in servidores:

        nome_instancia = j["instancia"]
        nome_microsservico = j["microsservico"]

        with open('yearly-data.csv', 'r', encoding='utf-8') as arquivo_lido:
            lido = csv.DictReader(arquivo_lido, delimiter=';')
            dia = 1

            for i in lido:
                hora_aleatoria = random.randint(0,23)
                minuto_aleatorio = random.randint(0,59)
                segundo_aleatorio = random.randint(0,59)
                data_hora = f"{i['date']} {hora_aleatoria}:{minuto_aleatorio}:{segundo_aleatorio}"

                multiplicador = float(i['infra_multiplicator'])

                esforco = (multiplicador - (-2.0)) / 4
                if(esforco > 1.0):
                    esforco = 1.0
                elif(esforco < 0.0):
                    esforco = 0.0

                variacao = random.uniform(-2.0,2.0)

                porcentagem_cpu = round((10.0 + (esforco * 80.0)) + variacao + round(random.uniform(5.3, -2.7),1), 2)
                if(porcentagem_cpu > 99.0):
                    porcentagem_cpu = 99.0
        
                frequencia_cpu = round((1.8 + (esforco * 2.0)) + variacao +round(random.uniform(2.2,-1.9),1), 2)
                if(frequencia_cpu < 1.8):
                    frequencia_cpu = 1.8
     
                porcentagem_ram = round((30 + (esforco * 60)) + variacao + round(random.uniform(5.3, -2.7),1), 2)
                if(porcentagem_ram > 90):
                    porcentagem_ram = 90
                if(porcentagem_ram < 30):
                    porcentagem_ram = 30

                porcentagem_mem_swap = round(((esforco**2) * 35.0) + variacao, 2)

                qtd_processos = ((220 + (esforco * 180))+variacao) + random.randint(-30, -10)

                if(esforco >= 0.6):
                    qtd_zumbis = random.choice([0, 0, 1])
                else:
                    qtd_zumbis = 0

                bytes_upload = round(((0.5 + esforco*45)+ variacao + (random.uniform(5.3, -2.7))), 2)
                if(bytes_upload < 0.5):
                    bytes_upload = 0.5

                valor = round((random.uniform(7.5, -13.7) + (255.0 * esforco)), 2)

                bytes_download = round((1.0 + esforco*200)+ variacao + random.uniform(5.3, -2.7), 2)

                if(bytes_download < 1.0):
                    bytes_download = 1.0

                disco = round((disco_inicial - (dia * 0.15)) - (esforco * 2.0), 2)
                dia+=1
      
                dados_dia = [
                    nome_instancia,
                    nome_microsservico,
                    porcentagem_cpu,
                    frequencia_cpu,
                    porcentagem_ram,
                    porcentagem_mem_swap,
                    qtd_processos,
                    qtd_zumbis,
                    bytes_upload,
                    bytes_download,
                    disco,
                    data_hora,
                    valor
                    ]

                exhibit(dados_dia)
                store(dados_dia)
                time.sleep(0.1)
        


def exhibit(data):
  line_instancia = f'Nome da instância: {data[0]}'
  line_micro_servico = f'Nome microsservico: {data[1]}'
  line_cpu_percent = f'Uso atual da CPU: {data[2]}%'
  line_cpu_frequency = f'Frequência atual da CPU: {data[3]} GHz'
  line_ram_percent = f'Uso atual de memória RAM: {data[4]}%'
  line_swap_memory_percent = f'Uso atual da memória swap: {data[5]}%'
  line_processes_qtd = f'Quantidade atual de processos ativos: {data[6]}'
  line_zombie = f'Quantidade de processos zumbis: {data[7]}'
  line_upload_bytes = f'Tráfego atual de upload de bytes da rede: {data[8]} Mbps'
  line_download_bytes = f'Tráfego atual de download de bytes da rede: {data[9]} Mbps'
  line_disk = f'Espaço livre em disco: {data[10]} GiB'
  line_timestamp = f'Momento de captura: {data[11]}'
  line_value_month = f'Média estipulada no mês: {data[12]}'

  print(f"""
    ----------------------------------------------------------------
    | {line_instancia:<60} |
    | {line_micro_servico:<60} |
    | {line_cpu_percent:<60} |
    | {line_cpu_frequency:<60} |
    | {line_ram_percent:<60} |
    | {line_swap_memory_percent:<60} |
    | {line_processes_qtd:<60} |
    | {line_zombie:<60} |
    | {line_upload_bytes:<60} |
    | {line_download_bytes:<60} |
    | {line_disk:<60} |
    | {line_timestamp:<60} |
    | {line_value_month:<60} |
    ----------------------------------------------------------------
    """)

def store(data):
  with open("simulacao_ano_v2.csv", 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow([data[0],data[1],data[2],data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],data[11],data[12]])

capture()
