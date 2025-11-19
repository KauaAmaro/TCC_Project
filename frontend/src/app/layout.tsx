import './globals.css'

export const metadata = {
  title: 'Leitor de Códigos de Barras',
  description: 'Sistema de leitura de códigos de barras via stream de câmera IP',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}