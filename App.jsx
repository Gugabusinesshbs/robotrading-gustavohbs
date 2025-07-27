import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'
import { TrendingUp, TrendingDown, Activity, DollarSign, BarChart3, Settings, Play, Pause, AlertCircle } from 'lucide-react'
import './App.css'

// URL base da API - ajustar conforme necessário
const API_BASE = 'http://localhost:5000/api/trading'

function App() {
  const [isTrading, setIsTrading] = useState(false)
  const [currentPrice, setCurrentPrice] = useState(50000)
  const [prediction, setPrediction] = useState({ direction: 'ALTA', confidence: 0.75 })
  const [balance, setBalance] = useState(1000)
  const [totalTrades, setTotalTrades] = useState(0)
  const [winRate, setWinRate] = useState(0)
  const [priceData, setPriceData] = useState([])
  const [recentTrades, setRecentTrades] = useState([])
  const [analytics, setAnalytics] = useState({})
  const [settings, setSettings] = useState({})
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  // Função para buscar dados da API
  const fetchData = async () => {
    try {
      // Buscar status do sistema
      const statusResponse = await fetch(`${API_BASE}/status`)
      const statusData = await statusResponse.json()
      
      setIsTrading(statusData.is_active)
      setCurrentPrice(statusData.current_price)
      setBalance(statusData.balance)
      setTotalTrades(statusData.total_trades)
      setWinRate(statusData.win_rate)

      // Buscar predição atual
      const predictionResponse = await fetch(`${API_BASE}/prediction`)
      const predictionData = await predictionResponse.json()
      setPrediction(predictionData)

      // Buscar histórico de preços
      const priceResponse = await fetch(`${API_BASE}/price-history`)
      const priceHistoryData = await priceResponse.json()
      setPriceData(priceHistoryData)

      // Buscar trades recentes
      const tradesResponse = await fetch(`${API_BASE}/recent-trades`)
      const tradesData = await tradesResponse.json()
      setRecentTrades(tradesData)

      // Buscar analytics
      const analyticsResponse = await fetch(`${API_BASE}/analytics`)
      const analyticsData = await analyticsResponse.json()
      setAnalytics(analyticsData)

      // Buscar configurações
      const settingsResponse = await fetch(`${API_BASE}/settings`)
      const settingsData = await settingsResponse.json()
      setSettings(settingsData)

      // Buscar logs
      const logsResponse = await fetch(`${API_BASE}/logs`)
      const logsData = await logsResponse.json()
      setLogs(logsData)

      setLoading(false)
    } catch (error) {
      console.error('Erro ao buscar dados da API:', error)
      setLoading(false)
    }
  }

  // Buscar dados iniciais e configurar atualização automática
  useEffect(() => {
    fetchData()
    
    // Atualizar dados a cada 3 segundos
    const interval = setInterval(fetchData, 3000)
    
    return () => clearInterval(interval)
  }, [])

  const toggleTrading = async () => {
    try {
      const response = await fetch(`${API_BASE}/toggle`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      const data = await response.json()
      setIsTrading(data.is_active)
    } catch (error) {
      console.error('Erro ao alternar trading:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Carregando sistema de trading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Trading Dashboard</h1>
            <p className="text-slate-300">Sistema de Trading Automatizado com IA</p>
          </div>
          <div className="flex items-center gap-4">
            <Badge variant={isTrading ? "default" : "secondary"} className="px-4 py-2">
              <Activity className="w-4 h-4 mr-2" />
              {isTrading ? 'ATIVO' : 'PARADO'}
            </Badge>
            <Button 
              onClick={toggleTrading}
              variant={isTrading ? "destructive" : "default"}
              size="lg"
            >
              {isTrading ? <Pause className="w-4 h-4 mr-2" /> : <Play className="w-4 h-4 mr-2" />}
              {isTrading ? 'Parar Trading' : 'Iniciar Trading'}
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Preço Atual BTC/USDT</CardTitle>
              <DollarSign className="h-4 w-4 text-slate-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">${currentPrice.toLocaleString()}</div>
              <p className="text-xs text-slate-400">
                {prediction.direction === 'ALTA' ? '+' : '-'}0.5% da última hora
              </p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Saldo</CardTitle>
              <DollarSign className="h-4 w-4 text-slate-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">${balance.toFixed(2)}</div>
              <p className="text-xs text-green-400">
                {analytics.total_return > 0 ? '+' : ''}{analytics.total_return}% total
              </p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Total de Trades</CardTitle>
              <BarChart3 className="h-4 w-4 text-slate-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">{totalTrades}</div>
              <p className="text-xs text-slate-400">
                {recentTrades.length} recentes
              </p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Taxa de Acerto</CardTitle>
              <TrendingUp className="h-4 w-4 text-slate-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">{(winRate * 100).toFixed(1)}%</div>
              <p className="text-xs text-green-400">
                Baseado em {recentTrades.length} trades
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chart Section */}
          <div className="lg:col-span-2">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Gráfico de Preços BTC/USDT</CardTitle>
                <CardDescription className="text-slate-400">
                  Dados em tempo real com predições da IA
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={priceData}>
                      <defs>
                        <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis dataKey="time" stroke="#9CA3AF" />
                      <YAxis stroke="#9CA3AF" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px',
                          color: '#F9FAFB'
                        }} 
                      />
                      <Area 
                        type="monotone" 
                        dataKey="price" 
                        stroke="#8884d8" 
                        fillOpacity={1} 
                        fill="url(#colorPrice)" 
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* AI Prediction */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  Predição da IA
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300">Direção:</span>
                    <Badge 
                      variant={prediction.direction === 'ALTA' ? 'default' : 'destructive'}
                      className="flex items-center"
                    >
                      {prediction.direction === 'ALTA' ? 
                        <TrendingUp className="w-4 h-4 mr-1" /> : 
                        <TrendingDown className="w-4 h-4 mr-1" />
                      }
                      {prediction.direction}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300">Confiança:</span>
                    <span className="text-white font-bold">
                      {(prediction.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                      style={{ width: `${prediction.confidence * 100}%` }}
                    ></div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recent Trades */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Trades Recentes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentTrades.map((trade) => (
                    <div key={trade.id} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Badge 
                          variant={trade.direction === 'ALTA' ? 'default' : 'destructive'}
                          className="text-xs"
                        >
                          {trade.direction}
                        </Badge>
                        <span className="text-slate-300 text-sm">{trade.time}</span>
                        {trade.type === 'MANUAL' && (
                          <Badge variant="outline" className="text-xs">MANUAL</Badge>
                        )}
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge 
                          variant={trade.result === 'WIN' ? 'default' : 'destructive'}
                          className="text-xs"
                        >
                          {trade.result}
                        </Badge>
                        <span className={`text-sm font-bold ${
                          trade.profit > 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          ${trade.profit.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Tabs Section */}
        <div className="mt-8">
          <Tabs defaultValue="analytics" className="w-full">
            <TabsList className="grid w-full grid-cols-3 bg-slate-800/50">
              <TabsTrigger value="analytics" className="text-slate-300">Analytics</TabsTrigger>
              <TabsTrigger value="settings" className="text-slate-300">Configurações</TabsTrigger>
              <TabsTrigger value="logs" className="text-slate-300">Logs</TabsTrigger>
            </TabsList>
            
            <TabsContent value="analytics" className="mt-6">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Análise de Performance</CardTitle>
                  <CardDescription className="text-slate-400">
                    Estatísticas detalhadas do sistema de trading
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                      <div className={`text-3xl font-bold ${analytics.total_return >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {analytics.total_return >= 0 ? '+' : ''}{analytics.total_return}%
                      </div>
                      <div className="text-slate-400">Retorno Total</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-400">{analytics.sharpe_ratio}</div>
                      <div className="text-slate-400">Sharpe Ratio</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-purple-400">{analytics.max_drawdown}%</div>
                      <div className="text-slate-400">Max Drawdown</div>
                    </div>
                  </div>
                  <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${analytics.total_profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        ${analytics.total_profit}
                      </div>
                      <div className="text-slate-400">Lucro Total</div>
                    </div>
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${analytics.avg_profit_per_trade >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        ${analytics.avg_profit_per_trade}
                      </div>
                      <div className="text-slate-400">Lucro Médio/Trade</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="settings" className="mt-6">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Configurações do Sistema</CardTitle>
                  <CardDescription className="text-slate-400">
                    Ajuste os parâmetros do algoritmo de trading
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-300">Valor por Trade:</span>
                      <span className="text-white">${settings.trade_amount}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-300">Stop Loss:</span>
                      <span className="text-white">{settings.stop_loss}%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-300">Take Profit:</span>
                      <span className="text-white">{settings.take_profit}%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-300">Confiança Mínima:</span>
                      <span className="text-white">{(settings.min_confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-300">Max Trades/Dia:</span>
                      <span className="text-white">{settings.max_trades_per_day}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="logs" className="mt-6">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Logs do Sistema</CardTitle>
                  <CardDescription className="text-slate-400">
                    Histórico de atividades e eventos
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 font-mono text-sm">
                    {logs.map((log, index) => (
                      <div key={index} className={`${
                        log.level === 'INFO' ? 'text-green-400' :
                        log.level === 'WARNING' ? 'text-yellow-400' :
                        log.level === 'ERROR' ? 'text-red-400' :
                        'text-blue-400'
                      }`}>
                        [{log.timestamp}] {log.message}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}

export default App

