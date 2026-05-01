import { cn } from "@/lib/utils"

export default function PageHeader({ title, description, className, children }) {
  return (
    <div className={cn("space-y-1", className)}>
      {title && <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>}
      {description && <p className="text-sm text-muted-foreground">{description}</p>}
      {children}
    </div>
  )
}
