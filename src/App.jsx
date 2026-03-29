import React, { useState, useEffect } from 'react';

const Dashboard = () => {
    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd');
                const result = await response.json();
                setData(result);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) return <div style={{ color: '#fff' }}>Loading...</div>;
    if (error) return <div style={{ color: '#ff0000' }}>Error fetching data</div>;

    return (
        <div style={{ backgroundColor: '#1a1a1a', color: '#fff', padding: '20px' }}>
            <h1 style={{ textAlign: 'center' }}>Cryptocurrency Dashboard</h1>
            <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '20px' }}>
                <button style={{ backgroundColor: '#4CAF50', color: '#fff', padding: '10px' }}>Assets</button>
                <button style={{ backgroundColor: '#008CBA', color: '#fff', padding: '10px' }}>Markets</button>
                <button style={{ backgroundColor: '#f44336', color: '#fff', padding: '10px' }}>Portfolio</button>
            </div>
            <div>
                {data.map((coin) => (
                    <div key={coin.id} style={{ border: '1px solid #fff', margin: '10px', padding: '10px' }}>
                        <h2>{coin.name} ({coin.symbol.toUpperCase()})</h2>
                        <p>Current Price: ${coin.current_price}</p>
                        <p>Market Cap: ${coin.market_cap}</p>
                        <p>24h Change: {coin.price_change_percentage_24h}%</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;