import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { NextUIProvider } from '@nextui-org/react'
import Header from '@/components/Header'

function MyApp({ Component, pageProps }: AppProps) {

  return (
    <NextUIProvider>
        <div className="px-4 sm:px-2 md:px-8 lg:px-12">
            <Header/>
            <Component {...pageProps} />
        </div>
    </NextUIProvider>
  )
}

export default MyApp