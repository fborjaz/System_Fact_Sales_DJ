document.addEventListener('DOMContentLoaded', function (e) {
  let $supplier = document.getElementById("id_supplier");
  let $detailBody = document.getElementById('detalle');
  let $product = document.getElementById('product');
  let $btnAdd = document.getElementById("btnAdd");
  let $btnSave = document.getElementById("btnSave");
  let $form = document.getElementById("frmSale");
  let detailPurchase = [];
  let sub = 0;

  // Initialize supplier select element
  if ($supplier) {
    $supplier.selectedIndex = 1;
  }

  // Initialize purchase details if they exist
  if (typeof detail_purchases !== 'undefined' && detail_purchases.length > 0) {
    detailPurchase = detail_purchases.map(item => {
      let { product: id, product__description: description, quantify, cost, subtotal: sub, iva } = item;
      return {
        id: parseInt(id),
        description,
        cost: parseFloat(cost),
        quantify: parseFloat(quantify),
        iva: parseFloat(iva),
        sub: parseFloat(sub)
      };
    });
    present();
    totals();
  }

  // Function to calculate details
  const calculation = (id, description, iva, cost, quantify) => {
    const product = detailPurchase.find(prod => prod.id === id);
    if (product) {
      if (!confirm(`¿Ya existe ingresado ${product.description} => Desea actualizarlo?`)) return;
      quantify += product.quantify;
      detailPurchase = detailPurchase.filter(prod => prod.id !== id);
    }
    iva = iva > 0 ? ((cost * quantify) * (iva / 100)).toFixed(2) : "0";
    iva = parseFloat(iva);
    sub = (cost * quantify + iva).toFixed(2);
    sub = parseFloat(sub);
    detailPurchase.push({ id, description, cost, quantify, iva, sub });
    present();
    totals();
  };

  // Handle product change
  const productChange = (e) => {
    const selectedOption = e.target.selectedOptions[0];
    const cost = selectedOption.getAttribute('data-cost');
    document.getElementById('cost').value = cost;  // Changed 'price' to 'cost'
    console.log(cost)
  };
 
  if ($product) {
    $product.addEventListener('change', productChange);
    productChange({ target: $product });
  }

  // Function to delete a product
  const deleteProduct = (id) => {
    detailPurchase = detailPurchase.filter((item) => item.id !== id);
    present();
    totals();
  };

  // Present purchase details in table
  function present() {
    if ($detailBody) {
      $detailBody.innerHTML = "";
      detailPurchase.forEach((product) => {
        $detailBody.innerHTML += `<tr class="dark:text-gray-400 bg-white border-b dark:bg-[#0b1121] dark:border-secundario hover:bg-gray-50 dark:hover:bg-[#121c33]">
              <td>${product.id}</td>
              <td>${product.description}</td>
              <td>${product.cost.toFixed(2)}</td>
              <td>${product.quantify.toFixed(2)}</td>
              <td>${product.iva.toFixed(2)}</td>
              <td>${product.sub.toFixed(2)}</td>
              <td class="text-center">
                  <button rel="rel-delete" data-id="${product.id}" class="text-red-600 dark:text-red-500"><i class="fa-solid fa-trash"></i></button>
              </td>
            </tr>`;
      });
    }
  }

  // Calculate totals
  function totals() {
    const result = detailPurchase.reduce((acc, product) => {
      acc.iva += product.iva;
      acc.sub += product.sub;
      return acc;
    }, { iva: 0, sub: 0 });
    document.getElementById('id_subtotal').value = (result.sub - result.iva).toFixed(2);
    document.getElementById('id_iva').value = result.iva.toFixed(2);
    document.getElementById('id_total').value = result.sub.toFixed(2);
  }

  // Save purchase
  async function savePurchase(urlPost, urlSuccess) {
    const formData = new FormData($form);
    formData.append("detail", JSON.stringify(detailPurchase));

    let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
      const res = await fetch(urlPost, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrf,
        },
        body: formData
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP error! Status: ${res.status}, Response: ${text}`);
      }

      const post = await res.json();
      alert(post.msg);
      window.location.href = urlSuccess;
    } catch (error) {
      alert("Error: " + error.message);
    }
  }

  // Handle form submission
  if ($form) {
    $form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (parseFloat(document.getElementById('id_total').value) > 0.00) {
        await savePurchase(save_url, '/purchase/purchase_list/');
      } else {
        alert("!!!Faltan datos de productos para grabar la compra!!!");
      }
    });
  }

  // Add product to detail
  if ($btnAdd) {
    $btnAdd.addEventListener('click', () => {
      let quantify = parseInt(document.getElementById('quantify').value);
      let stock = parseInt($product.options[$product.selectedIndex].dataset.stock);
      if (quantify > 0 && quantify <= stock) {
        let idProd = parseInt($product.value);
        let cost = parseFloat(document.getElementById('cost').value.replace(',', '.'));
        let iva = parseFloat($product.options[$product.selectedIndex].dataset.iva.replace(',', '.'));
        let description = $product.options[$product.selectedIndex].text;
        calculation(idProd, description, iva, cost, quantify);
      } else {
        alert(`Cantidad negativa o superior al stock:[${stock}]`);
      }
    });
  }

  // Handle product removal event
  if ($detailBody) {
    $detailBody.addEventListener('click', (e) => {
      const button = e.target.closest('button[rel=rel-delete]');
      if (button) deleteProduct(parseInt(button.getAttribute('data-id')));
    });
  }
});
