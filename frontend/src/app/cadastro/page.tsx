'use client'

import { useState } from 'react'
import Link from 'next/link'



export default function Cadastro() {
  const [codigoBarras, setCodigoBarras] = useState('')
  const [descricao, setDescricao] = useState('')

  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<'success' | 'error'>('success')

  const API_BASE = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000'





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


    </div>
  )
}