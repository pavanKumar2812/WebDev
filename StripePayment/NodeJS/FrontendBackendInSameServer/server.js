// 1. THIS MUST BE THE VERY FIRST LINE
require("dotenv").config();

// 2. This console.log is good for debugging and confirms the variable name
// It should now show your actual secret key, not 'undefined'
console.log('Value of STRIPE_SECRET_KEY:', process.env.STRIPE_SECRET_KEY);

const express = require("express");
const app = express();
const cors = require("cors"); // Import the cors package

app.use(express.json()); // Enable parsing of JSON request bodies
app.use(express.static("public")); // Serve static files from the 'public' directory
app.use(cors()); // Enable CORS for all routes (important for frontend-backend communication)

// Initialize Stripe with your secret key
// This line will fail if process.env.STRIPE_SECRET_KEY is undefined or invalid
const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);

const storeItems = new Map([
    [1, { priceInRupees: 1000, name: "Blue Half Pant"}],
    [2, { priceInRupees: 1899, name: "N-Blue Half Pant"}],
]);

// Endpoint to create a Stripe Checkout Session
app.post("/create-checkout-session", async (req, res) => {
    try {
        // Create an array of line items for the Stripe Checkout Session
        // This example assumes the frontend sends an array of item IDs and quantities
        const lineItems = req.body.items.map(item => {
            const storeItem = storeItems.get(item.id);
            if (!storeItem) {
                // If an item is not found, throw an error
                throw new Error(`Item with ID ${item.id} not found.`);
            }
            return {
                price_data: {
                    currency: "inr", // Indian Rupees
                    product_data: {
                        name: storeItem.name,
                    },
                    // Stripe expects amount in the smallest currency unit (e.g., paise for INR)
                    unit_amount: storeItem.priceInRupees * 100,
                },
                quantity: item.quantity,
            };
        });

        // Create the Stripe Checkout Session
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ["card"], // Only allow card payments for this example
            mode: "payment", // This is a one-time payment
            line_items: lineItems,
            // Use SERVER_URL from .env for redirect URLs
            success_url: `${process.env.SERVER_URL}/success.html`,
            cancel_url: `${process.env.SERVER_URL}/cancel.html`,
        });
        console.log("Checkout session created:", session.id);
        // Send the session URL back to the client
        res.json({ url: session.url });

    } catch (e) {
        // If an error occurs, send a 500 status code and the error message
        console.error("Error creating checkout session:", e);
        res.status(500).json({ error: e.message });
    }
});

// Start the server
app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
