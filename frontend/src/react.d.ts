declare module 'react' {
  export = React;
  export as namespace React;
}

declare module 'react/jsx-runtime' {
  export const jsx: any;
  export const jsxs: any;
  export const Fragment: any;
}

declare module 'lucide-react' {
  export const ShieldAlert: any;
  export const LayoutDashboard: any;
  export const TriangleAlert: any;
  export const Building2: any;
  export const Network: any;
  export const Sliders: any;
  export const CheckSquare: any;
  export const Ticket: any;
  export const FileText: any;
  export const Activity: any;
}

declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}
