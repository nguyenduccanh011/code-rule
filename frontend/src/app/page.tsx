'use client';

import { useEffect, useState } from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';

export default function Home() {
  const [stockList, setStockList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStockList = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/stocks/list`);
        if (!response.ok) {
          throw new Error('Failed to fetch stock list');
        }
        const data = await response.json();
        setStockList(data.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchStockList();
  }, []);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Stock Platform
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Stock List
              </Typography>
              {loading ? (
                <Typography>Loading...</Typography>
              ) : error ? (
                <Typography color="error">{error}</Typography>
              ) : (
                <pre>{JSON.stringify(stockList, null, 2)}</pre>
              )}
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
} 