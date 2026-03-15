import Link from "next/link";
import Image from "next/image";

type LogoProps = {
  /** Altura del logo en píxeles */
  height?: number;
  /** Si false, el logo no es un enlace */
  linkToHome?: boolean;
  /** Clases adicionales para el contenedor */
  className?: string;
};

export function Logo({ height = 36, linkToHome = true, className = "" }: LogoProps) {
  const img = (
    <Image
      src="/Logo.png"
      alt="Tramitup"
      width={height * 3}
      height={height}
      className="object-contain"
      priority
    />
  );

  if (linkToHome) {
    return (
      <Link href="/" className={`inline-flex items-center ${className}`} aria-label="Tramitup - Ir al inicio">
        {img}
      </Link>
    );
  }

  return <span className={`inline-flex items-center ${className}`}>{img}</span>;
}
