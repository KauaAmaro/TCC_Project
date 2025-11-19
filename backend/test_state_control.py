#!/usr/bin/env python3

def test_state_logic():
    """Testa a lógica de controle de estado sem câmera"""
    
    print("=== TESTE DE LÓGICA DE CONTROLE DE ESTADO ===")
    
    # Simular sequência de frames
    frames_simulados = [
        [],                    # Frame 1: nenhum código
        ["ABC123"],           # Frame 2: código ABC123 aparece
        ["ABC123"],           # Frame 3: mesmo código (não deve contar)
        ["ABC123"],           # Frame 4: mesmo código (não deve contar)
        [],                   # Frame 5: código desaparece
        ["ABC123"],           # Frame 6: código reaparece (deve contar)
        ["ABC123", "XYZ789"], # Frame 7: dois códigos
        ["XYZ789"],           # Frame 8: apenas XYZ789
        [],                   # Frame 9: nenhum código
    ]
    
    codigos_ativos = set()
    contagens = {}
    
    for frame_num, codigos_detectados in enumerate(frames_simulados, 1):
        codigos_atuais = set(codigos_detectados)
        
        print(f"\n📹 Frame {frame_num}")
        print(f"   Detectados: {codigos_atuais}")
        print(f"   Ativos antes: {codigos_ativos}")
        
        # Processar novas entradas
        novas_entradas = codigos_atuais - codigos_ativos
        for codigo in novas_entradas:
            contagens[codigo] = contagens.get(codigo, 0) + 1
            print(f"   ✅ CONTANDO: {codigo} (total: {contagens[codigo]})")
        
        # Log de saídas
        saidas = codigos_ativos - codigos_atuais
        for codigo in saidas:
            print(f"   🚪 SAÍDA: {codigo}")
        
        # Atualizar estado
        codigos_ativos = codigos_atuais.copy()
        print(f"   Ativos depois: {codigos_ativos}")
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   Contagens: {contagens}")
    print(f"   ABC123 deve ter 2 contagens (frames 2 e 6)")
    print(f"   XYZ789 deve ter 1 contagem (frame 7)")
    
    # Validar resultado
    expected = {"ABC123": 2, "XYZ789": 1}
    if contagens == expected:
        print("   ✅ TESTE PASSOU!")
    else:
        print(f"   ❌ TESTE FALHOU! Esperado: {expected}")

if __name__ == "__main__":
    test_state_logic()