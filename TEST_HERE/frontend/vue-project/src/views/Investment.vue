<template>
    <div>
        <h2>Invest in Assets</h2>
        <form @submit.prevent="makeInvestment">
            <label>Asset Type:</label>
            <select v-model="investment.asset_type">
                <option value="stock">Stock</option>
                <option value="bond">Bond</option>
                <option value="etf">ETF</option>
            </select>
            <label>Amount:</label>
            <input v-model="investment.amount" type="number" required />
            <button type="submit">Invest</button>
        </form>
        <div>
            <h3>Your Investments</h3>
            <ul>
                <li v-for="inv in investments" :key="inv.id">
                    {{ inv.asset_type }} - {{ inv.amount }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import api from '../api';

export default {
    data() {
        return {
            investment: { asset_type: '', amount: 0 },
            investments: []
        };
    },
    methods: {
        async fetchInvestments() {
            const response = await api.get('/investments/');
            this.investments = response.data;
        },
        async makeInvestment() {
            await api.post('/investments/', this.investment);
            this.fetchInvestments();
        },
    },
    created() {
        this.fetchInvestments();
    },
};
</script>
