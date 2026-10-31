import { useEffect, useState } from "react";

export default function Lista() {
  const [items, setItems] = useState();

  useEffect(() => {
    fetch("/api/items")
      .then((r) => r.json())
      .then((data) => setItems(data.items));
  }, []);

  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.nombre}</li>
      ))}
    </ul>
  );
}
