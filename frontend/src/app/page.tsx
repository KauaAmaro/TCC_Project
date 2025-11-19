'use client'

import { useState, useEffect } from 'react'

interface Leitura {
  id: number
  codigo_barras: string
  descricao: string
  quantidade: number
  data_hora: string
}

export default function Home() {
  const [leituras, setLeituras] = useState<Leitura[]>([])
  const [streamUrl, setStreamUrl] = useState('http://192.168.1.244:8080/video')
  const [isStreaming, setIsStreaming] = useState(false)
  const [loading, setLoading] = useState(false)

  const API_BASE = 'http://localhost:8000'

  useEffect(() => {
    const interval = setInterval(fetchLeituras, 2000)
    fetchLeituras()
    return () => clearInterval(interval)
  }, [])

  const fetchLeituras = async () => {
    try {
      const response = await fetch(`${API_BASE}/leituras`)
      const data = await response.json()
      setLeituras(data)
    } catch (error) {
      console.error('Erro ao buscar leituras:', error)
    }
  }

  const startStream = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/start-stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: streamUrl })
      })
      
      if (response.ok) {
        setIsStreaming(true)
        alert('Stream iniciado com sucesso!')
      } else {
        alert('Erro ao iniciar stream')
      }
    } catch (error) {
      alert('Erro ao conectar com o backend')
    }
    setLoading(false)
  }

  const stopStream = async () => {
    try {
      await fetch(`${API_BASE}/stop-stream`, { method: 'POST' })
      setIsStreaming(false)
      alert('Stream parado')
    } catch (error) {
      alert('Erro ao parar stream')
    }
  }

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  return (
    <div className="container">
      <h1 style={{ marginBottom: '30px', textAlign: 'center' }}>
        Leitor de Códigos de Barras
      </h1>

      <div className="card">
        <h2 style={{ marginBottom: '15px' }}>Configuração do Stream</h2>
        <input
          type="text"
          className="input"
          value={streamUrl}
          onChange={(e) => setStreamUrl(e.target.value)}
          placeholder="URL do stream da câmera IP"
          disabled={isStreaming}
        />
        <div>
          {!isStreaming ? (
            <button 
              className="btn btn-primary" 
              onClick={startStream}
              disabled={loading}
            >
              {loading ? 'Iniciando...' : 'Iniciar Leitura'}
            </button>
          ) : (
            <button className="btn btn-danger" onClick={stopStream}>
              Parar Leitura
            </button>
          )}
          <span style={{ marginLeft: '15px', color: isStreaming ? 'green' : 'red' }}>
            Status: {isStreaming ? 'Ativo' : 'Inativo'}
          </span>
        </div>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h2>Leituras ({leituras.length})</h2>
          <div>
            <a href="/cadastro" style={{ textDecoration: 'none', marginRight: '10px' }}>
              <button className="btn btn-primary">📝 Cadastrar Produtos</button>
            </a>
            <a href="/relatorio" style={{ textDecoration: 'none' }}>
              <button className="btn btn-primary">📊 Ver Relatório</button>
            </a>
          </div>
        </div>
        {leituras.length === 0 ? (
          <p>Nenhuma leitura encontrada</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Código de Barras</th>
                <th>Descrição</th>
                <th>Quantidade</th>
                <th>Data/Hora</th>
              </tr>
            </thead>
            <tbody>
              {leituras.map((leitura) => (
                <tr key={leitura.id}>
                  <td>{leitura.codigo_barras}</td>
                  <td>{leitura.descricao}</td>
                  <td>{leitura.quantidade}</td>
                  <td>{formatDateTime(leitura.data_hora)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}