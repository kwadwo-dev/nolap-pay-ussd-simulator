# NOLAP Pay USSD Simulator

## Description
NOLAP Pay is a Python-based command-line application that simulates a mobile money USSD service (*1145#). 
It allows users to perform common mobile money operations securely and interactively.  

### Features
- **Account Management**: Create a new account or log in with an existing phone number and PIN.
- **Money Transfer**: Send money to other users with transaction fees applied.
- **Buy Airtime**: Purchase airtime for yourself directly from your balance.
- **Withdraw & Deposit**: Withdraw funds with fees or deposit money into your account.
- **Check Balance**: View your current account balance (PIN required).
- **Change PIN**: Update your account PIN for security.

> Note: All data is stored temporarily in memory; restarting the app will reset all accounts.

### Transaction Fees
| Transaction | Rate | Maximum Fee |
|------------|------|-------------|
| Transfer   | 0.75% | GHS 15 (for amounts ≥ 2000) |
| Withdraw   | 1%    | GHS 20 (for amounts ≥ 2000) |

---

## How to Run the App
1. Ensure you have **Python 3.8+** installed on your machine.
2. Clone or download this repository:
   ```bash
   git clone <your-repo-url>


## Author
**Donzy Chaka**
