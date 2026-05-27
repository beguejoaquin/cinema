import { fetchProducts } from "@/lib/api";

interface Product {
  id: number;
  name: string;
  description: string;
  price: string;
}

export default async function Home() {
  let products: Product[] = [];
  try {
    products = await fetchProducts();
  } catch (error) {
    console.error("Error fetching products:", error);
  }
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Products</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.id} className="border rounded-lg p-6 shadow-md">
            <h2 className="text-xl font-semibold">{product.name}</h2>
            <p className="text-gray-600 mt-2">{product.description}</p>
            <p className="text-green-600 font-bold mt-4">${product.price}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
