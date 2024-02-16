const Discord = require('discord.js');
const client = new Discord.Client();

// Define the possible status messages
const statusMessages = [
  'sleeping',
  'eating',
  'doing sport'
];

// Function to generate a random status message
function generateStatusMessage() {
  const randomIndex = Math.floor(Math.random() * statusMessages.length);
  return statusMessages[randomIndex];
}

// Set the initial status message
let currentStatus = generateStatusMessage();

// Function to update the bot's status message
function updateStatus() {
  const newStatus = generateStatusMessage();
  if (newStatus !== currentStatus) {
    client.user.setActivity(newStatus);
    currentStatus = newStatus;
  }
}

// Event triggered when the bot is ready
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
  updateStatus();
  setInterval(updateStatus, 60000); // Update status every minute
});

// Log in to Discord using your bot token
client.login('MTIwODAwMTY0Mjc3NTk2OTg2Mg.GRx_4z.4Vc71MZDzsE7UO8Qz8opwE_Xu8ecNfuDGziyMI');
