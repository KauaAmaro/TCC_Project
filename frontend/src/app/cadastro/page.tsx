'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Produto {
  id: number
  codigo_barras: string
  descricao: string
  data_cadastro: string
}

export default function Cadastro() {
  const [codigoBarras, setCodigoBarras] = useState('')
  const [descricao, setDescricao] = useState('')
  const [produtos, setProdutos] = useState<Produto[]>([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<'success' | 'error'>('success')

  const API_BASE = 'http://localhost:8000'

  useEffect(() => {
    fetchProdutos()
  }, [])

  const fetchProdutos = async () => {
    try {
      const response = await fetch(`${API_BASE}/produtos`)
      if (response.ok) {
        const data = await response.json()
        setProdutos(data)
      }
    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!codigoBarras.trim() || !descricao.trim()) {
      setMessage('Todos os campos são obrigatórios')
      setMessageType('error')
      return
    }

    setLoading(true)
    setMessage('')

    try {
      const response = await fetch(`${API_BASE}/produtos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          codigo_barras: codigoBarras.trim(),
          descricao: descricao.trim()
        })
      })

      if (response.ok) {
        setMessage('Produto cadastrado com sucesso!')
        setMessageType('success')
        setCodigoBarras('')
        setDescricao('')
        fetchProdutos() // Atualizar lista
      } else if (response.status === 409) {
        setMessage('Código de barras já cadastrado')
        setMessageType('error')
      } else {
        setMessage('Erro ao cadastrar produto')
        setMessageType('error')
      }
    } catch (error) {
      setMessage('Erro de conexão com o servidor')
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '30px' }}>
        <Link href="/" style={{ marginRight: '20px', textDecoration: 'none', color: '#007bff' }}>
          ← Voltar
        </Link>
        <h1>Cadastro de Produtos</h1>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '20px' }}>Novo Produto</h2>
        
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Código de Barras *
            </label>
            <input
              type="text"
              className="input"
              value={codigoBarras}
              onChange={(e) => setCodigoBarras(e.target.value)}
              placeholder="Ex: 7891000100103"
              disabled={loading}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Descrição do Produto *
            </label>
            <input
              type="text"
              className="input"
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
              placeholder="Ex: Água Mineral 500ml"
              disabled={loading}
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Salvando...' : 'Salvar Produto'}
          </button>
        </form>

        {message && (
          <div style={{ 
            marginTop: '15px', 
            padding: '10px', 
            borderRadius: '4px',
            backgroundColor: messageType === 'success' ? '#d4edda' : '#f8d7da',
            color: messageType === 'success' ? '#155724' : '#721c24',
            border: `1px solid ${messageType === 'success' ? '#c3e6cb' : '#f5c6cb'}`
          }}>
            {message}
          </div>
        )}
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h2>Produtos Cadastrados ({produtos.length})</h2>
          <button className="btn btn-primary" onClick={fetchProdutos}>
            Atualizar
          </button>
        </div>

        {produtos.length === 0 ? (
          <p>Nenhum produto cadastrado ainda.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Código de Barras</th>
                <th>Descrição</th>
                <th>Data Cadastro</th>
              </tr>
            </thead>
            <tbody>
              {produtos.map((produto) => (
                <tr key={produto.id}>
                  <td>{produto.codigo_barras}</td>
                  <td>{produto.descricao}</td>
                  <td>{formatDate(produto.data_cadastro)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}