'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface RelatorioData {
  descricao: string
  quantidade: number
}

export default function Relatorio() {
  const [dados, setDados] = useState<RelatorioData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [debugInfo, setDebugInfo] = useState('')

  const API_BASE = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000'

  useEffect(() => {
    console.log('🔄 Componente Relatório montado, iniciando fetch...')
    fetchRelatorio()
  }, [])

  const fetchRelatorio = async () => {
    try {
      console.log('📡 Iniciando requisição para:', `${API_BASE}/relatorio`)
      setLoading(true)
      setError('')
      setDebugInfo('Conectando ao backend...')
      
      const response = await fetch(`${API_BASE}/relatorio`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      console.log('📊 Resposta recebida:', {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries())
      })
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('❌ Erro HTTP:', response.status, errorText)
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('📄 Dados recebidos:', data)
      
      // Validar estrutura dos dados
      if (!Array.isArray(data)) {
        throw new Error('Dados não são um array')
      }
      
      // Validar cada item
      const dadosValidos = data.filter(item => 
        item && 
        typeof item.descricao === 'string' && 
        typeof item.quantidade === 'number'
      )
      
      if (dadosValidos.length !== data.length) {
        console.warn('⚠️ Alguns itens foram filtrados por estrutura inválida')
      }
      
      setDados(dadosValidos)
      setError('')
      setDebugInfo(`${dadosValidos.length} itens carregados com sucesso`)
      
    } catch (err: any) {
      const errorMsg = err.message || 'Erro desconhecido'
      console.error('❌ Erro completo:', err)
      setError(`Falha ao carregar relatório: ${errorMsg}`)
      setDebugInfo(`Erro: ${errorMsg}`)
      setDados([])
    } finally {
      setLoading(false)
    }
  }

  const maxQuantidade = Math.max(...dados.map(d => d.quantidade), 1)

  return (
    <div className="container">
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '30px' }}>
        <Link href="/" style={{ marginRight: '20px', textDecoration: 'none', color: '#007bff' }}>
          ← Voltar
        </Link>
        <div>
          <h1>Relatório - Leituras por Produto</h1>
          {debugInfo && (
            <small style={{ color: '#666', fontSize: '12px' }}>
              Debug: {debugInfo}
            </small>
          )}
        </div>
      </div>

      {loading && (
        <div className="card">
          <p>Carregando dados...</p>
        </div>
      )}

      {error && (
        <div className="card" style={{ borderLeft: '4px solid #dc3545' }}>
          <p style={{ color: '#dc3545' }}>{error}</p>
          <button className="btn btn-primary" onClick={fetchRelatorio}>
            Tentar Novamente
          </button>
        </div>
      )}

      {!loading && !error && dados.length === 0 && (
        <div className="card">
          <p>Nenhuma leitura registrada até o momento.</p>
        </div>
      )}

      {!loading && !error && dados.length > 0 && (
        <div className="card">
          <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>Gráfico de Leituras</h2>
            <button className="btn btn-primary" onClick={fetchRelatorio}>
              Atualizar
            </button>
          </div>
          
          <div style={{ marginBottom: '30px' }}>
            <div style={{ display: 'flex', marginBottom: '10px', fontSize: '14px', color: '#666' }}>
              <div style={{ width: '200px' }}>Produto</div>
              <div style={{ flex: 1 }}>Quantidade</div>
            </div>
            
            {dados.map((item, index) => (
              <div key={index} style={{ marginBottom: '15px' }}>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
                  <div style={{ 
                    width: '200px', 
                    fontSize: '14px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap'
                  }}>
                    {item.descricao}
                  </div>
                  <div style={{ 
                    flex: 1, 
                    height: '30px', 
                    backgroundColor: '#f0f0f0',
                    borderRadius: '4px',
                    position: 'relative',
                    marginLeft: '10px'
                  }}>
                    <div style={{
                      height: '100%',
                      width: `${(item.quantidade / maxQuantidade) * 100}%`,
                      backgroundColor: '#007bff',
                      borderRadius: '4px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'flex-end',
                      paddingRight: '8px',
                      color: 'white',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      minWidth: '40px'
                    }}>
                      {item.quantidade}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div style={{ fontSize: '14px', color: '#666' }}>
            Total de produtos: {dados.length} | 
            Total de leituras: {dados.reduce((sum, item) => sum + item.quantidade, 0)}
          </div>
        </div>
      )}
    </div>
  )
}