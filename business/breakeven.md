```markdown
# breakeven.md

## Cost per Active User (CAU)
- **Compute**: $0.025/user/month (AWS EC2 t3.medium instances for 100M core-seconds/month)
- **Storage**: $0.005/user/month (1GB SSD storage per user)
- **Bandwidth**: $0.01/user/month (50GB outbound transfer/month)
- **Total CAU**: **$0.045/user/month**

## Pricing Tiers
| Tier | Price/Mo | Users | Features |
|------|----------|-------|----------|
| Starter | $9/mo | 1000 | 10 projects, 1GB storage, 100GB bandwidth |
| Pro | $29/mo | 500 | 50 projects, 10GB storage, 1TB bandwidth |
| Enterprise | $99/mo | 100 | Unlimited projects, 100GB storage, unlimited bandwidth |

## CAC Range
- **Average CAC**: $45-$75 (includes marketing, sales, support)
- **CAC Distribution**: 
  - 40% paid via referral program ($20 avg)
  - 35% via organic growth ($10 avg)
  - 25% via paid advertising ($60 avg)

## LTV Estimate
- **LTV Calculation**:
  - Avg. Monthly Revenue per User = $29 (Pro tier)
  - Churn Rate = 5% monthly
  - Customer Lifetime = 1/(0.05) = 20 months
  - LTV = $29 × 20 = **$580**
- **LTV/CAC Ratio**: 580/60 ≈ **9.7:1**

## Break-even Users Count
- **Break-even Point**:
  - Fixed Costs (dev, ops, support, etc.) = $10,000/month
  - Revenue per user = $29 (Pro tier)
  - Break-even users = 10,000 / 29 ≈ **345 users**
- **Break-even Month**: 3rd month (assuming ramp-up from 0 to 345 users)

## Path to $10K MRR
- **Target MRR**: $10,000/month
- **Required Users**:
  - 100 Enterprise users ($99 × 100 = $9,900)
  - 10 additional Pro users ($29 × 10 = $290)
  - Total: **110 users**
- **Path**:
  - Month 1: 50 Pro users ($1,450)
  - Month 2: 100 Pro users ($2,900)
  - Month 3: 110 Pro users ($3,190)
  - Month 4: 110 Enterprise users ($10,890)
```