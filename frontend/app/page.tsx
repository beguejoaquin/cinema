"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { categories, movies } from "@/lib/placeholder-data";

export default async function Home() {
  return (
    <>
      <h1 className="mx-auto my-5 text-4xl w-fit">CINEMA</h1>
      <div id="movies">
        {movies.map((movie) => (
          <Card key={movie.id} onClick={() => console.log("shupa")}>
            {/* <img
              src="https://avatar.vercel.sh/shadcn1"
              alt="Event cover"
              className="relative z-20 aspect-video w-full object-cover brightness-60 grayscale dark:brightness-40"
            /> */}
            <CardHeader>
              <CardTitle>{movie.title}</CardTitle>
            </CardHeader>
          </Card>
        ))}
      </div>
    </>
  );
}
