if (document.readyState == 'loading') {
  document.addEventListener('DOMContentLoaded', ready)
} else {
  ready()
}

function Abrir_Carrinho(){
  var slides = document.getElementById("carrinho_rest");
  
  slides.className = "carrinho_restaurante_aberto"
  console.log('foi')
}

function FecharCarrinho(){
  var slides = document.getElementById("carrinho_rest");
  
  slides.className = "carrinho_restaurante_fechado"
}


var totalAmount = "0,00"

function ready() {
  // Botão remover produto
  const removeCartProductButtons = document.getElementsByClassName("remove-product-button")
  for (var i = 0; i < removeCartProductButtons.length; i++) {
    removeCartProductButtons[i].addEventListener("click", removeProduct)
  }

  // Mudança valor dos inputs
  const quantityInputs = document.getElementsByClassName("product-qtd-input")
  for (var i = 0; i < quantityInputs.length; i++) {
    quantityInputs[i].addEventListener("change", checkIfInputIsNull)
  }

  // Botão add produto ao carrinho
  const addToCartButtons = document.getElementsByClassName("add_carrinho")
  for (var i = 0; i < addToCartButtons.length; i++) {
    addToCartButtons[i].addEventListener("click", addProductToCart)

  }

  // Botão comprar
  const purchaseButton = document.getElementsByClassName("purchase-button")[0]
  purchaseButton.addEventListener("click", makePurchase)
}

function removeProduct(event) {
  event.target.parentElement.parentElement.remove()
  updateTotal()
}

function checkIfInputIsNull(event) {
  if (event.target.value === "0") {
    event.target.parentElement.parentElement.remove()
  }

  updateTotal()
}

function addProductToCart(event) {
  const button = event.target
  const productInfos = button.parentElement
  const productImage = productInfos.getElementsByClassName("Prod_img")[0].src
  const productName = productInfos.getElementsByClassName("Prod_nome")[0].innerText
  const productPrice = productInfos.getElementsByClassName("Prod_preco")[0].innerText

  const productsCartNames = document.getElementsByClassName("cart-product-title")
  for (var i = 0; i < productsCartNames.length; i++) {
    if (productsCartNames[i].innerText === productName) {
      productsCartNames[i].parentElement.parentElement.getElementsByClassName("product-qtd-input")[0].value++
      updateTotal()
      return
    }
  }

  let newCartProduct = document.createElement("tr")
  newCartProduct.classList.add("cart-product")

  newCartProduct.innerHTML =
    `
      <td class="product-identification">
        <img src="${productImage}" alt="${productName}" class="cart-product-image"><br>
        <strong class="cart-product-title">${productName}</strong>
      </td>
      <td>
        <span class="cart-product-price">${productPrice}</span>
      </td>
      <td>
        <input type="number" value="1" min="0" class="product-qtd-input">
        <button type="button" class="remove-product-button">Remover</button>
      </td>
    `
  
  const tableBody = document.querySelector(".cart-table tbody")
  tableBody.append(newCartProduct)
  updateTotal()

  newCartProduct.getElementsByClassName("remove-product-button")[0].addEventListener("click", removeProduct)
  newCartProduct.getElementsByClassName("product-qtd-input")[0].addEventListener("change", checkIfInputIsNull)
}

function makePurchase() {
  if (totalAmount === "0,00") {
    alert("Seu carrinho está vazio!")
  } else {   
    alert(
      `
        Obrigado pela sua compra!
        Valor do pedido: R$${totalAmount}\n
        Volte sempre :)
      `
    )



    document.querySelector(".cart-table tbody").innerHTML = ""
    updateTotal()
  }
}

// Atualizar o valor total do carrinho
function updateTotal() {
  const cartProducts = document.getElementsByClassName("cart-product")
  totalAmount = 0

  for (var i = 0; i < cartProducts.length; i++) {
    const productPrice = cartProducts[i].getElementsByClassName("cart-product-price")[0].innerText.replace("R$", "").replace(",", ".")
    const productQuantity = cartProducts[i].getElementsByClassName("product-qtd-input")[0].value

    totalAmount += productPrice * productQuantity
  }
  
  totalAmount = totalAmount.toFixed(2)
  totalAmount = totalAmount.replace(".", ",")
  document.querySelector(".cart-total-container span").innerText = "R$" + totalAmount
}


function getHello() {
  const url = 'http://127.0.0.1:5000/Restaurante'
  fetch(url)
  .then(response => response.json())  
  .then(json => {
      console.log(json);
      document.getElementById("demo").innerHTML = JSON.stringify(json)
  })
}

function makePurchase() {
let submit 


const url = 'http://127.0.0.1:5000/carrinho';  
const dadosCarrinho = {
    totalAmount: totalAmount,
    produtos: []
};



const cartProducts = document.getElementsByClassName("cart-product");
for (let i = 0; i < cartProducts.length; i++) {
    const productName = cartProducts[i].getElementsByClassName("cart-product-title")[0].innerText;
    const productPrice = cartProducts[i].getElementsByClassName("cart-product-price")[0].innerText;
    const productQuantity = cartProducts[i].getElementsByClassName("product-qtd-input")[0].value;

    dadosCarrinho.produtos.push({
        nome: productName,
        preco: productPrice,
        quantidade: productQuantity
    });
}

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(dadosCarrinho),
})
.then(response => response.json())
.then(data => {
    console.log('Sucesso:', data);
    alert("Seu pedido foi enviado com sucesso!");
    
    document.querySelector(".cart-table tbody").innerHTML = "";
    updateTotal();
})



.catch((error) => {
    console.error('Erro:', error);
    alert("Ocorreu um erro ao enviar seu pedido.");
});
}


