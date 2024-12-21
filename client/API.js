function ListAuctions() {

};

async function fetchLast10EnglishAuctions() {
    const query = `
      query ListLast10EnglishAuctions {
        tokens {
          liveAuctions(last: 10) {
            nodes {
              slug
              currentPrice
              endDate
              bestBid {
                amounts {
                  wei
                }
                bidder {
                  ... on User {
                    nickname
                  }
                }
              }
              minNextBid
              anyCards {
                slug
                name
                rarity
              }
            }
          }
        }
      }
    `;
  
    const response = await fetch('https://api.sorare.com/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer <${token}>`,
        // 'APIKEY': '<YourOptionalAPIKey>'
      },
      body: JSON.stringify({ query })
    });
  
    const data = await response.json();
    console.log(data);
    data.data.tokens.liveAuctions.nodes.forEach((auction) => {
      WriteOut(auction);
    });
  }
  
  //fetchLast10EnglishAuctions().catch(error => console.error(error));