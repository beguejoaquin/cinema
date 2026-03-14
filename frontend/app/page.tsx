"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { categories, movies } from "@/lib/placeholder-data";

export default function Home() {
  return (
    <>
      <h1 className="mx-auto my-5 text-4xl w-fit">CINEMA</h1>
      <div id="movies" className="w-3/4 mx-auto grid grid-cols-6 gap-2">
        {movies.map((movie) => (
          <Card key={movie.id} onClick={() => console.log("shupa")}>
            <img
              src={movie.poster}
              alt="Event cover"
              className="relative z-20 w-full object-cover"
            />
            <CardHeader>
              <CardTitle>{movie.title}</CardTitle>
            </CardHeader>
          </Card>
        ))}
      </div>
    </>
  );
}
